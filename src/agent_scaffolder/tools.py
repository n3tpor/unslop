from __future__ import annotations
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from solace_ai_connector.common.log import log

# -----------------------------
# Utilities
# -----------------------------
_VALID_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "-", name.strip().lower()).strip("-").replace("--", "-")

def _ensure_ident(s: str, kind: str) -> str:
    if not _VALID_IDENT.match(s):
        raise ValueError(f"Invalid {kind} identifier: '{s}'")
    return s

def _now_tag() -> str:
    return datetime.utcnow().strftime("%Y%m%d-%H%M%S")

def _resolve_base(tool_context) -> Path:
    """
    Resolve a stable base dir for writing source files.
    Preference order:
      1) app_base_path
      2) component_base_path
      3) repo root inferred from this file (../../)
    """
    if tool_context is not None:
        app_base = getattr(tool_context, "app_base_path", None)
        if app_base:
            return Path(app_base).resolve()
        comp_base = getattr(tool_context, "component_base_path", None)
        if comp_base:
            return Path(comp_base).resolve()
    # Fallback: two levels up from current module (adjust if your layout differs)
    return Path(__file__).resolve().parents[2]

def _render_param_sig(params: List[Dict[str, Any]]) -> str:
    """
    Render python signature params after *simple*, adding type hints and defaults.
    Always includes 'tool_context=None, tool_config: Optional[Dict[str, Any]] = None' at the end.
    """
    rendered = []
    for p in params:
        nm = _ensure_ident(p["name"], "parameter")
        typ = p.get("type", "Any")
        if "default" in p:
            default_repr = repr(p["default"])
            rendered.append(f"{nm}: {typ} = {default_repr}")
        else:
            rendered.append(f"{nm}: {typ}")
    rendered.append("tool_context=None")
    rendered.append("tool_config: Optional[Dict[str, Any]] = None")
    return ", ".join(rendered)

def _render_docstring(desc: str, params: List[Dict[str, Any]], returns: Dict[str, Any]) -> str:
    lines = ['"""', desc.strip()]
    if params:
        lines.append("")
        lines.append("Args:")
        for p in params:
            nm = p["name"]
            typ = p.get("type", "Any")
            pd = p.get("description", "")
            lines.append(f"  {nm} ({typ}): {pd}")
    if returns:
        lines.append("")
        lines.append("Returns:")
        rt = returns.get("type", "Any")
        rd = returns.get("description", "")
        lines.append(f"  {rt}: {rd}")
    lines.append('"""')
    return "\n    ".join(lines)

def _default_body(return_type: str | None) -> str:
    # Minimal body that compiles and helps during wiring
    if return_type and return_type.lower() in {"dict", "mapping"}:
        return "    result = {\"status\": \"ok\", \"note\": \"Replace with real logic\"}\n    return result\n"
    return "    return \"OK (replace with real logic)\"\n"

def _function_exists(file_text: str, fname: str) -> bool:
    pattern = re.compile(rf"^async\s+def\s+{re.escape(fname)}\s*\(", re.MULTILINE)
    return bool(pattern.search(file_text))

def _render_function_block(spec: Dict[str, Any]) -> str:
    fname = _ensure_ident(spec["function_name"], "function")
    desc = spec.get("description", "No description provided.")
    params = spec.get("params", [])
    returns = spec.get("returns", {"type": "Any", "description": ""})
    body = spec.get("body")  # optional source body (without def/async)

    sig = _render_param_sig(params)
    doc = _render_docstring(desc, params, returns)

    block = []
    block.append(f"async def {fname}({sig}) -> {returns.get('type','Any')}:")
    block.append(f"    {doc}")
    # Simple trace log
    block.append(f"    log.info(\"[{fname}] called\")")
    # Inject custom body or default
    if body:
        # indent provided body to 4 spaces and ensure trailing newline
        body_lines = [("    " + line) if line.strip() else line for line in body.splitlines()]
        block.extend(body_lines)
        if not body.endswith("\n"):
            block.append("")
    else:
        block.append(_default_body(returns.get("type")))
    return "\n".join(block) + "\n\n"

def _render_header(module_title: str) -> str:
    return f"""# Auto-generated tool stubs for {module_title}
from __future__ import annotations
from typing import Any, Dict, List, Optional
from solace_ai_connector.common.log import log

"""

def _render_yaml_tool_block(module_path: str, fn_name: str, description: str = "") -> str:
    desc = description or f"{fn_name} tool."
    return (
        "- tool_type: python\n"
        f"  component_module: \"{module_path}\"\n"
        "  component_base_path: .\n"
        f"  function_name: \"{fn_name}\"\n"
        f"  tool_description: \"{desc}\"\n"
    )

# -----------------------------
# Public entrypoint
# -----------------------------
async def define_dynamic_tools(
    agent_name: str,
    tools: List[Dict[str, Any]],
    overwrite: bool = False,
    tool_context=None,
    tool_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Dynamically create tool functions for an agent under: src/<agent_slug>/tools.py

    Args:
      agent_name: Logical agent name; becomes folder slug: src/<slug>/
      tools: List of tool specs like:
        [
          {
            "function_name": "summarize_text",
            "description": "Summarize text to N words.",
            "params": [
              {"name": "text", "type": "str", "description": "The input text."},
              {"name": "max_words", "type": "int", "default": 100, "description": "Word cap."}
            ],
            "returns": {"type": "dict", "description": "Summary payload."},
            # optional: "body": "    # your code here\n    return {\"summary\": text[:80]}"
          },
          ...
        ]
      overwrite: If True, replace existing functions with the same name; else skip.
    Returns:
      {
        "status": "success",
        "module_path": "src.<slug>.tools",
        "py_file": "/abs/path/src/<slug>/tools.py",
        "created": ["fn1", ...],
        "skipped": ["fnX", ...],
        "yaml_tools_block": "<pasteable YAML>"
      }
    """
    if not agent_name:
        return {"status": "error", "error": "agent_name is required"}
    if not tools:
        return {"status": "error", "error": "tools must be a non-empty list"}

    slug = _slugify(agent_name).replace("-", "_")
    _ensure_ident(slug if slug[0].isalpha() else f"_{slug}", "module")

    base = _resolve_base(tool_context)
    src_dir = base / "src" / slug
    py_file = src_dir / "tools.py"
    init_file = src_dir / "__init__.py"
    module_path = f"src.{slug}.tools"

    src_dir.mkdir(parents=True, exist_ok=True)
    init_file.write_text("", encoding="utf-8") if not init_file.exists() else None

    # Load or initialize the module file
    if py_file.exists():
        text = py_file.read_text(encoding="utf-8")
    else:
        text = _render_header(module_title=agent_name)

    created, skipped = [], []
    for spec in tools:
        try:
            fname = _ensure_ident(spec["function_name"], "function")
        except Exception as e:
            skipped.append(f"{spec.get('function_name','<missing>')} (invalid: {e})")
            continue

        exists = _function_exists(text, fname)
        if exists and not overwrite:
            skipped.append(fname)
            continue

        # If overwriting, remove old function block (basic replace by pattern)
        if exists and overwrite:
            text = re.sub(
                rf"^async\s+def\s+{re.escape(fname)}\s*\([^\)]*\)\s*->[\s\S]*?\n(?=^async\s+def|\Z)",
                "",
                text,
                flags=re.MULTILINE,
            )

        text += _render_function_block(spec)
        created.append(fname)

    # Write final file
    py_file.write_text(text, encoding="utf-8")
    log.info("[define_dynamic_tools] Wrote %s", py_file)

    # Register artifact(s)
    artifact_ids: List[str] = []
    try:
        if tool_context and getattr(tool_context, "artifact_service", None):
            art = tool_context.artifact_service.create_file_artifact(
                file_path=str(py_file),
                display_name=f"{slug}_tools_{_now_tag()}.py",
                mime_type="text/x-python",
            )
            if art and hasattr(art, "id"):
                artifact_ids.append(art.id)
    except Exception as e:
        log.warning("[define_dynamic_tools] Could not create artifact: %s", e)

    # Compose YAML tool block suggestions
    yaml_blocks = []
    for spec in tools:
        fn = spec.get("function_name")
        if not fn or not _VALID_IDENT.match(fn):
            continue
        yaml_blocks.append(_render_yaml_tool_block(module_path, fn, spec.get("description","")))
    yaml_tools_block = "\n".join(yaml_blocks)

    return {
        "status": "success",
        "module_path": module_path,
        "py_file": str(py_file.resolve()),
        "created": created,
        "skipped": skipped,
        "artifact_ids": artifact_ids,
        "yaml_tools_block": yaml_tools_block,
    }
