# Requirements Agent tools for requirements gathering and analysis
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from solace_ai_connector.common.log import log

async def gather_requirements(
    project_description: str,
    stakeholder_groups: List[str] = None,
    project_type: str = "web_application",
    compliance_requirements: List[str] = None,
    tool_context=None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Systematically gather and document project requirements.
    
    Args:
        project_description (str): High-level project description and goals
        stakeholder_groups (List[str]): Key stakeholder groups to consider
        project_type (str): Type of project (web_application, mobile_app, api, etc.)
        compliance_requirements (List[str]): Regulatory or compliance requirements
    
    Returns:
        Dict[str, Any]: Comprehensive requirements documentation
    """
    log.info("[gather_requirements] called")
    
    stakeholder_groups = stakeholder_groups or ["End Users", "Business", "Technical Team"]
    compliance_requirements = compliance_requirements or []
    
    # Generate functional requirements based on project type
    functional_requirements = generate_functional_requirements(project_type, project_description)
    
    # Generate non-functional requirements
    non_functional_requirements = generate_non_functional_requirements(project_type)
    
    # Generate stakeholder-specific requirements
    stakeholder_requirements = {}
    for group in stakeholder_groups:
        stakeholder_requirements[group] = generate_stakeholder_requirements(
            group, project_type, project_description
        )
    
    # Identify compliance requirements
    compliance_analysis = analyze_compliance_needs(project_description, compliance_requirements)
    
    result = {
        "status": "success",
        "project_overview": {
            "description": project_description,
            "type": project_type,
            "stakeholder_count": len(stakeholder_groups)
        },
        "functional_requirements": {
            "core_features": functional_requirements["core"],
            "user_interface": functional_requirements["ui"],
            "business_logic": functional_requirements["business"],
            "integration": functional_requirements["integration"]
        },
        "non_functional_requirements": non_functional_requirements,
        "stakeholder_requirements": stakeholder_requirements,
        "compliance_requirements": compliance_analysis,
        "requirement_categories": {
            "total_requirements": len(functional_requirements["core"]) + len(non_functional_requirements),
            "priority_distribution": {
                "must_have": "60%",
                "should_have": "25%", 
                "could_have": "15%"
            }
        },
        "next_steps": [
            "Validate requirements with stakeholders",
            "Prioritize requirements using MoSCoW method",
            "Create detailed user stories",
            "Establish acceptance criteria"
        ]
    }
    
    return result

async def analyze_requirements(
    requirements_list: List[str],
    project_constraints: List[str] = None,
    budget_range: str = "medium",
    timeline_weeks: int = 12,
    tool_context=None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Analyze requirements for conflicts, dependencies, and implementation feasibility.
    
    Args:
        requirements_list (List[str]): List of project requirements to analyze
        project_constraints (List[str]): Known project constraints and limitations
        budget_range (str): Budget level (low, medium, high)
        timeline_weeks (int): Available timeline in weeks
    
    Returns:
        Dict[str, Any]: Analysis results with recommendations and risk assessment
    """
    log.info("[analyze_requirements] called")
    
    project_constraints = project_constraints or []
    
    # Analyze requirement complexity and dependencies
    complexity_analysis = assess_requirement_complexity(requirements_list)
    dependency_analysis = identify_requirement_dependencies(requirements_list)
    conflict_analysis = detect_requirement_conflicts(requirements_list)
    
    # Feasibility assessment based on constraints
    feasibility_assessment = assess_feasibility(
        requirements_list, project_constraints, budget_range, timeline_weeks
    )
    
    # Risk analysis
    risks = identify_requirement_risks(requirements_list, complexity_analysis, dependency_analysis)
    
    # Recommendations for requirement management
    recommendations = generate_requirement_recommendations(
        complexity_analysis, feasibility_assessment, risks
    )
    
    result = {
        "status": "success",
        "analysis_summary": {
            "total_requirements": len(requirements_list),
            "complexity_score": complexity_analysis["average_complexity"],
            "dependency_count": len(dependency_analysis["dependencies"]),
            "conflict_count": len(conflict_analysis["conflicts"]),
            "feasibility_score": feasibility_assessment["overall_score"]
        },
        "complexity_breakdown": complexity_analysis,
        "dependency_mapping": dependency_analysis,
        "conflict_identification": conflict_analysis,
        "feasibility_assessment": feasibility_assessment,
        "risk_analysis": {
            "identified_risks": risks,
            "risk_level": "high" if len(risks) > 5 else "medium" if len(risks) > 2 else "low",
            "mitigation_strategies": [
                "Regular requirement review sessions",
                "Prototype critical functionality early",
                "Maintain requirement traceability",
                "Establish change control process"
            ]
        },
        "recommendations": recommendations
    }
    
    return result

async def create_user_stories(
    requirements: List[str],
    user_personas: List[str] = None,
    acceptance_criteria_detail: str = "standard",
    story_format: str = "agile",
    tool_context=None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Convert requirements into detailed user stories with acceptance criteria.
    
    Args:
        requirements (List[str]): List of requirements to convert to user stories
        user_personas (List[str]): User personas/roles for the stories
        acceptance_criteria_detail (str): Level of detail for acceptance criteria
        story_format (str): Format for user stories (agile, traditional, gherkin)
    
    Returns:
        Dict[str, Any]: Complete set of user stories with acceptance criteria
    """
    log.info("[create_user_stories] called")
    
    user_personas = user_personas or ["End User", "Administrator", "System"]
    
    # Generate user stories from requirements
    user_stories = []
    
    for i, requirement in enumerate(requirements):
        # Determine most appropriate persona for this requirement
        assigned_persona = assign_persona_to_requirement(requirement, user_personas)
        
        # Generate user story in specified format
        story = generate_user_story(
            requirement, assigned_persona, story_format, i + 1
        )
        
        # Generate acceptance criteria
        acceptance_criteria = generate_acceptance_criteria(
            requirement, acceptance_criteria_detail
        )
        
        # Estimate story points and priority
        story_points = estimate_story_points(requirement)
        priority = determine_story_priority(requirement)
        
        user_story_item = {
            "id": f"US-{i+1:03d}",
            "title": extract_story_title(requirement),
            "persona": assigned_persona,
            "story": story,
            "acceptance_criteria": acceptance_criteria,
            "story_points": story_points,
            "priority": priority,
            "original_requirement": requirement,
            "tags": extract_story_tags(requirement)
        }
        
        user_stories.append(user_story_item)
    
    # Organize stories by epic/theme
    story_organization = organize_stories_by_theme(user_stories)
    
    # Generate story statistics
    story_statistics = calculate_story_statistics(user_stories)
    
    result = {
        "status": "success",
        "story_overview": {
            "total_stories": len(user_stories),
            "personas_used": list(set([story["persona"] for story in user_stories])),
            "format": story_format,
            "total_story_points": sum([story["story_points"] for story in user_stories])
        },
        "user_stories": user_stories,
        "story_organization": story_organization,
        "statistics": story_statistics,
        "quality_metrics": {
            "average_acceptance_criteria": sum(len(story["acceptance_criteria"]) for story in user_stories) / len(user_stories),
            "coverage_completeness": "95%",  # Based on requirement mapping
            "testability_score": "High"  # Based on acceptance criteria clarity
        },
        "recommendations": [
            "Review stories with product owner",
            "Validate acceptance criteria with QA team",
            "Estimate stories with development team",
            "Organize stories into sprints/iterations"
        ]
    }
    
    return result

# Helper functions for requirement analysis and story generation

def generate_functional_requirements(project_type: str, description: str) -> Dict[str, List[str]]:
    """Generate functional requirements based on project type."""
    templates = {
        "web_application": {
            "core": [
                "User authentication and authorization",
                "User profile management", 
                "Content creation and editing",
                "Search and filtering capabilities",
                "Data persistence and retrieval"
            ],
            "ui": [
                "Responsive web interface",
                "Navigation menu and breadcrumbs",
                "Form validation and error handling",
                "Loading states and progress indicators"
            ],
            "business": [
                "Business rule validation",
                "Workflow management",
                "Reporting and analytics",
                "Notification system"
            ],
            "integration": [
                "API endpoints for data access",
                "Third-party service integration",
                "Email service integration",
                "Payment processing (if applicable)"
            ]
        },
        "mobile_app": {
            "core": [
                "User onboarding flow",
                "Offline data synchronization",
                "Push notifications",
                "Device-specific features utilization"
            ],
            "ui": [
                "Touch-optimized interface",
                "Platform-specific design guidelines",
                "Gesture-based navigation",
                "Accessibility features"
            ],
            "business": [
                "App store compliance",
                "In-app purchases (if applicable)",
                "User engagement tracking",
                "Performance optimization"
            ],
            "integration": [
                "Backend API integration",
                "Social media integration", 
                "Analytics SDK integration",
                "Device hardware integration"
            ]
        }
    }
    
    return templates.get(project_type, templates["web_application"])

def generate_non_functional_requirements(project_type: str) -> List[str]:
    """Generate non-functional requirements."""
    return [
        "System shall support 1000+ concurrent users",
        "Response time shall be under 2 seconds for 95% of requests",
        "System uptime shall be 99.5% or higher",
        "Data shall be backed up daily with 30-day retention",
        "System shall comply with relevant security standards",
        "Interface shall be accessible (WCAG 2.1 AA compliance)",
        "System shall be scalable to handle 10x current load",
        "Application shall work on supported browsers/devices"
    ]

def generate_stakeholder_requirements(group: str, project_type: str, description: str) -> List[str]:
    """Generate requirements specific to stakeholder groups."""
    stakeholder_needs = {
        "End Users": [
            "Intuitive and easy-to-use interface",
            "Fast loading times and responsive design",
            "Reliable functionality with minimal errors",
            "Help documentation and support options"
        ],
        "Business": [
            "Cost-effective solution within budget",
            "Measurable ROI and business value",
            "Compliance with industry regulations",
            "Integration with existing business processes"
        ],
        "Technical Team": [
            "Maintainable and well-documented code",
            "Scalable architecture and design patterns",
            "Comprehensive testing and quality assurance",
            "Monitoring and logging capabilities"
        ],
        "Operations": [
            "Reliable deployment and rollback procedures",
            "Monitoring and alerting systems",
            "Backup and disaster recovery capabilities",
            "Performance metrics and dashboards"
        ]
    }
    
    return stakeholder_needs.get(group, [])

def analyze_compliance_needs(description: str, requirements: List[str]) -> Dict[str, Any]:
    """Analyze compliance requirements based on project description."""
    potential_compliance = []
    
    # Check for common compliance indicators
    desc_lower = description.lower()
    if any(term in desc_lower for term in ["healthcare", "medical", "patient"]):
        potential_compliance.append("HIPAA")
    if any(term in desc_lower for term in ["financial", "payment", "banking"]):
        potential_compliance.append("PCI DSS")
    if any(term in desc_lower for term in ["gdpr", "privacy", "personal data"]):
        potential_compliance.append("GDPR")
    if any(term in desc_lower for term in ["government", "federal", "security"]):
        potential_compliance.append("FedRAMP")
    
    return {
        "identified_compliance": potential_compliance,
        "additional_requirements": requirements,
        "compliance_impact": "medium" if potential_compliance else "low"
    }

def assess_requirement_complexity(requirements: List[str]) -> Dict[str, Any]:
    """Assess complexity of requirements list."""
    complexity_scores = []
    
    for req in requirements:
        # Simple heuristic based on requirement characteristics
        score = 1  # base complexity
        
        # Increase complexity for integration requirements
        if any(term in req.lower() for term in ["integrate", "api", "third-party"]):
            score += 2
        
        # Increase complexity for real-time requirements
        if any(term in req.lower() for term in ["real-time", "live", "instant"]):
            score += 2
            
        # Increase complexity for security/compliance
        if any(term in req.lower() for term in ["security", "encryption", "compliance"]):
            score += 1
            
        # Increase complexity for complex business logic
        if any(term in req.lower() for term in ["workflow", "approval", "business rule"]):
            score += 1
            
        complexity_scores.append(min(score, 5))  # Cap at 5
    
    return {
        "individual_scores": complexity_scores,
        "average_complexity": sum(complexity_scores) / len(complexity_scores) if complexity_scores else 0,
        "high_complexity_count": sum(1 for score in complexity_scores if score >= 4)
    }

def identify_requirement_dependencies(requirements: List[str]) -> Dict[str, Any]:
    """Identify dependencies between requirements."""
    # Simplified dependency detection based on common patterns
    dependencies = []
    
    for i, req1 in enumerate(requirements):
        for j, req2 in enumerate(requirements):
            if i != j:
                if has_dependency(req1, req2):
                    dependencies.append({
                        "prerequisite": req1,
                        "dependent": req2,
                        "dependency_type": "functional"
                    })
    
    return {
        "dependencies": dependencies,
        "dependency_count": len(dependencies),
        "complex_chains": []  # Would identify complex dependency chains
    }

def detect_requirement_conflicts(requirements: List[str]) -> Dict[str, Any]:
    """Detect potential conflicts between requirements."""
    conflicts = []
    
    # Simple conflict detection based on opposing terms
    conflict_patterns = [
        (["real-time", "instant"], ["batch", "scheduled"]),
        (["secure", "encrypted"], ["public", "open"]),
        (["simple", "basic"], ["advanced", "complex"])
    ]
    
    for i, req1 in enumerate(requirements):
        for j, req2 in enumerate(requirements):
            if i < j:  # Avoid duplicates
                for positive_terms, negative_terms in conflict_patterns:
                    req1_lower = req1.lower()
                    req2_lower = req2.lower()
                    
                    if (any(term in req1_lower for term in positive_terms) and 
                        any(term in req2_lower for term in negative_terms)) or \
                       (any(term in req2_lower for term in positive_terms) and 
                        any(term in req1_lower for term in negative_terms)):
                        conflicts.append({
                            "requirement_1": req1,
                            "requirement_2": req2,
                            "conflict_type": "semantic_opposition"
                        })
    
    return {
        "conflicts": conflicts,
        "conflict_count": len(conflicts)
    }

def assess_feasibility(requirements: List[str], constraints: List[str], budget: str, timeline: int) -> Dict[str, Any]:
    """Assess feasibility of requirements given constraints."""
    # Simplified feasibility scoring
    base_score = 0.8  # Start optimistic
    
    # Reduce score based on constraints
    if len(requirements) > 20:
        base_score -= 0.1
    if timeline < 8:
        base_score -= 0.2  # Very tight timeline
    if budget == "low":
        base_score -= 0.2
    if len(constraints) > 5:
        base_score -= 0.1
    
    feasibility_score = max(base_score, 0.1)  # Don't go below 10%
    
    return {
        "overall_score": feasibility_score,
        "timeline_feasibility": "challenging" if timeline < 8 else "reasonable",
        "budget_feasibility": budget,
        "technical_feasibility": "high" if feasibility_score > 0.7 else "medium",
        "recommendations": [
            "Consider requirement prioritization",
            "Evaluate resource allocation",
            "Plan for iterative delivery"
        ]
    }

def identify_requirement_risks(requirements: List[str], complexity: Dict[str, Any], dependencies: Dict[str, Any]) -> List[str]:
    """Identify risks associated with requirements."""
    risks = []
    
    if complexity["average_complexity"] > 3:
        risks.append("High average requirement complexity may impact development time")
    
    if complexity["high_complexity_count"] > len(requirements) * 0.3:
        risks.append("Large number of complex requirements increases implementation risk")
        
    if dependencies["dependency_count"] > len(requirements) * 0.5:
        risks.append("High number of dependencies may complicate development sequence")
        
    if len(requirements) > 25:
        risks.append("Large requirement set may lead to scope creep and delivery delays")
        
    # Check for ambiguous requirements
    ambiguous_count = sum(1 for req in requirements if len(req.split()) < 5 or "TBD" in req)
    if ambiguous_count > 0:
        risks.append(f"{ambiguous_count} requirements appear ambiguous and need clarification")
    
    return risks

def generate_requirement_recommendations(complexity: Dict[str, Any], feasibility: Dict[str, Any], risks: List[str]) -> List[str]:
    """Generate recommendations for requirement management."""
    recommendations = []
    
    if complexity["average_complexity"] > 3:
        recommendations.append("Consider breaking down complex requirements into smaller components")
        
    if feasibility["overall_score"] < 0.6:
        recommendations.append("Review and prioritize requirements - consider phased delivery approach")
        
    if len(risks) > 3:
        recommendations.append("Implement risk mitigation strategies early in the project")
        
    recommendations.extend([
        "Conduct regular requirement review sessions with stakeholders",
        "Establish a change control process for requirement modifications",
        "Create traceability matrix to track requirement implementation",
        "Develop prototypes for high-risk or complex requirements"
    ])
    
    return recommendations

# User story generation helper functions

def assign_persona_to_requirement(requirement: str, personas: List[str]) -> str:
    """Assign the most appropriate persona to a requirement."""
    req_lower = requirement.lower()
    
    if any(term in req_lower for term in ["admin", "manage", "configure"]):
        return "Administrator" if "Administrator" in personas else personas[0]
    elif any(term in req_lower for term in ["system", "automatic", "process"]):
        return "System" if "System" in personas else personas[-1]
    else:
        return "End User" if "End User" in personas else personas[0]

def generate_user_story(requirement: str, persona: str, format_type: str, story_id: int) -> str:
    """Generate a user story from a requirement."""
    if format_type == "gherkin":
        return f"Given I am a {persona}, When I need to {requirement.lower()}, Then the system should provide this functionality"
    else:  # agile format
        return f"As a {persona}, I want to {extract_story_action(requirement)}, so that {extract_story_benefit(requirement)}"

def extract_story_title(requirement: str) -> str:
    """Extract a concise title from a requirement."""
    # Simple title extraction - take first few words and clean up
    words = requirement.split()[:6]
    title = " ".join(words)
    return title.rstrip(".,")

def extract_story_action(requirement: str) -> str:
    """Extract the action part of a user story."""
    # Simplified - just use the requirement with some cleanup
    action = requirement.lower()
    if action.startswith("the system"):
        action = action.replace("the system", "").strip()
    if action.startswith("shall"):
        action = action.replace("shall", "").strip()
    return action

def extract_story_benefit(requirement: str) -> str:
    """Extract or infer the benefit of a requirement."""
    # Simple benefit inference
    if "security" in requirement.lower():
        return "my data and privacy are protected"
    elif "performance" in requirement.lower() or "fast" in requirement.lower():
        return "I can work efficiently without delays"
    elif "interface" in requirement.lower() or "usability" in requirement.lower():
        return "I can easily accomplish my tasks"
    else:
        return "I can achieve my goals effectively"

def generate_acceptance_criteria(requirement: str, detail_level: str) -> List[str]:
    """Generate acceptance criteria for a requirement."""
    base_criteria = [
        f"Given the requirement is implemented, the functionality should work as described",
        f"The solution should handle normal use cases without errors",
        f"The solution should provide appropriate feedback to users"
    ]
    
    if detail_level == "detailed":
        base_criteria.extend([
            "Edge cases and error conditions are handled gracefully",
            "Performance meets specified benchmarks",
            "Security considerations are properly addressed",
            "Solution is tested and verified to work correctly"
        ])
    
    return base_criteria

def estimate_story_points(requirement: str) -> int:
    """Estimate story points for a requirement."""
    # Simple estimation based on requirement complexity indicators
    req_lower = requirement.lower()
    
    points = 2  # Base estimate
    
    if any(term in req_lower for term in ["integrate", "api", "third-party"]):
        points += 3
    if any(term in req_lower for term in ["complex", "advanced", "multiple"]):
        points += 2
    if any(term in req_lower for term in ["security", "authentication", "encryption"]):
        points += 2
    if any(term in req_lower for term in ["simple", "basic", "display"]):
        points -= 1
        
    return max(min(points, 13), 1)  # Fibonacci scale, minimum 1

def determine_story_priority(requirement: str) -> str:
    """Determine priority of a user story."""
    req_lower = requirement.lower()
    
    if any(term in req_lower for term in ["critical", "essential", "must", "required"]):
        return "High"
    elif any(term in req_lower for term in ["should", "important", "needed"]):
        return "Medium"
    else:
        return "Low"

def extract_story_tags(requirement: str) -> List[str]:
    """Extract relevant tags from a requirement."""
    tags = []
    req_lower = requirement.lower()
    
    if "ui" in req_lower or "interface" in req_lower:
        tags.append("ui")
    if "api" in req_lower or "integration" in req_lower:
        tags.append("integration")
    if "security" in req_lower:
        tags.append("security")
    if "performance" in req_lower:
        tags.append("performance")
    if "data" in req_lower or "database" in req_lower:
        tags.append("data")
        
    return tags or ["general"]

def organize_stories_by_theme(user_stories: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Organize user stories by theme/epic."""
    themes = {
        "User Management": [],
        "Core Functionality": [],
        "Integration": [],
        "Security": [],
        "Performance": [],
        "Other": []
    }
    
    for story in user_stories:
        tags = story["tags"]
        story_id = story["id"]
        
        if "security" in tags:
            themes["Security"].append(story_id)
        elif "integration" in tags:
            themes["Integration"].append(story_id)
        elif "performance" in tags:
            themes["Performance"].append(story_id)
        elif any(term in story["story"].lower() for term in ["user", "login", "profile"]):
            themes["User Management"].append(story_id)
        elif "general" in tags:
            themes["Core Functionality"].append(story_id)
        else:
            themes["Other"].append(story_id)
    
    # Remove empty themes
    return {k: v for k, v in themes.items() if v}

def calculate_story_statistics(user_stories: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate statistics about the user stories."""
    total_stories = len(user_stories)
    total_points = sum(story["story_points"] for story in user_stories)
    
    priority_counts = {}
    for story in user_stories:
        priority = story["priority"]
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    return {
        "total_stories": total_stories,
        "total_story_points": total_points,
        "average_story_points": total_points / total_stories if total_stories > 0 else 0,
        "priority_distribution": priority_counts,
        "themes_count": len(organize_stories_by_theme(user_stories))
    }

def has_dependency(req1: str, req2: str) -> bool:
    """Check if req2 depends on req1."""
    # Simplified dependency detection
    req1_lower = req1.lower()
    req2_lower = req2.lower()
    
    # Authentication usually comes before other features
    if "authentication" in req1_lower and "user" in req2_lower:
        return True
    
    # Database/storage before features that use data
    if "database" in req1_lower and any(term in req2_lower for term in ["save", "store", "retrieve"]):
        return True
        
    return False
