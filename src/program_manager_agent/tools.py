# Program Manager tools for project coordination and milestone management  
from __future__ import annotations
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from solace_ai_connector.common.log import log

async def create_project_plan(
    project_name: str,
    project_description: str,
    duration_weeks: int = 12,
    team_size: int = 5,
    priority: str = "medium",
    tool_context=None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create detailed project plans with milestones and deliverables.
    
    Args:
        project_name (str): Name of the project
        project_description (str): Detailed project description and scope
        duration_weeks (int): Expected project duration in weeks
        team_size (int): Number of team members
        priority (str): Project priority level (low, medium, high, critical)
    
    Returns:
        Dict[str, Any]: Comprehensive project plan with milestones and timeline
    """
    log.info("[create_project_plan] called")
    
    # Calculate key project phases as percentages of total duration
    phases = {
        "Planning & Discovery": 0.15,  # 15% of time
        "Design & Architecture": 0.20,  # 20% of time  
        "Development": 0.45,  # 45% of time
        "Testing & QA": 0.15,  # 15% of time
        "Deployment & Launch": 0.05   # 5% of time
    }
    
    start_date = datetime.now()
    milestones = []
    current_date = start_date
    
    for phase_name, time_allocation in phases.items():
        phase_duration = int(duration_weeks * time_allocation)
        phase_duration = max(1, phase_duration)  # Minimum 1 week per phase
        
        milestone = {
            "phase": phase_name,
            "start_date": current_date.strftime("%Y-%m-%d"),
            "end_date": (current_date + timedelta(weeks=phase_duration)).strftime("%Y-%m-%d"),
            "duration_weeks": phase_duration,
            "deliverables": get_phase_deliverables(phase_name),
            "success_criteria": get_phase_success_criteria(phase_name)
        }
        milestones.append(milestone)
        current_date += timedelta(weeks=phase_duration)
    
    # Risk assessment based on project characteristics
    risk_factors = assess_project_risks(duration_weeks, team_size, priority)
    
    result = {
        "status": "success",
        "project_overview": {
            "name": project_name,
            "description": project_description,
            "total_duration_weeks": duration_weeks,
            "team_size": team_size,
            "priority": priority,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "estimated_end_date": current_date.strftime("%Y-%m-%d")
        },
        "project_phases": milestones,
        "resource_allocation": {
            "team_composition": generate_team_roles(team_size),
            "weekly_capacity": f"{team_size * 40} hours",
            "total_effort_hours": team_size * 40 * duration_weeks
        },
        "risk_assessment": risk_factors,
        "communication_plan": {
            "daily_standups": "Every weekday, 15 minutes",
            "sprint_reviews": "Bi-weekly, 1 hour",
            "stakeholder_updates": "Weekly status reports",
            "milestone_reviews": "At end of each phase"
        }
    }
    
    return result

async def track_project_progress(
    project_name: str,
    current_phase: str,
    completed_tasks: int = 0,
    total_tasks: int = 100,
    team_velocity: float = 0.8,
    blockers: List[str] = None,
    tool_context=None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Monitor and track project progress with metrics and risk identification.
    
    Args:
        project_name (str): Name of the project being tracked
        current_phase (str): Current project phase
        completed_tasks (int): Number of completed tasks
        total_tasks (int): Total estimated tasks
        team_velocity (float): Team velocity (0.0-1.0 scale)
        blockers (List[str]): Current project blockers or issues
    
    Returns:
        Dict[str, Any]: Project status report with recommendations
    """
    log.info("[track_project_progress] called")
    
    blockers = blockers or []
    
    # Calculate progress metrics
    completion_percentage = (completed_tasks / max(total_tasks, 1)) * 100
    
    # Velocity assessment
    velocity_status = {
        "excellent": (0.9, 1.0),
        "good": (0.75, 0.9),
        "concerning": (0.6, 0.75),
        "critical": (0.0, 0.6)
    }
    
    velocity_rating = "good"
    for rating, (min_vel, max_vel) in velocity_status.items():
        if min_vel <= team_velocity < max_vel:
            velocity_rating = rating
            break
    
    # Risk indicators
    risks = []
    if team_velocity < 0.7:
        risks.append("Low team velocity - may miss deadlines")
    if len(blockers) > 3:
        risks.append("High number of blockers affecting progress")
    if completion_percentage < 20 and current_phase == "Development":
        risks.append("Behind schedule for current phase")
    
    # Generate recommendations
    recommendations = generate_progress_recommendations(
        velocity_rating, len(blockers), completion_percentage
    )
    
    result = {
        "status": "success",
        "project_name": project_name,
        "current_status": {
            "phase": current_phase,
            "completion_percentage": f"{completion_percentage:.1f}%",
            "completed_tasks": completed_tasks,
            "remaining_tasks": total_tasks - completed_tasks,
            "team_velocity": f"{team_velocity:.2f}",
            "velocity_rating": velocity_rating
        },
        "blockers_and_risks": {
            "active_blockers": blockers,
            "blocker_count": len(blockers),
            "identified_risks": risks,
            "risk_level": "high" if len(risks) > 2 else "medium" if risks else "low"
        },
        "forecasting": {
            "estimated_completion": "On track" if team_velocity > 0.8 else "At risk",
            "recommended_actions": recommendations,
            "next_milestone_risk": "low" if team_velocity > 0.75 else "medium"
        },
        "team_health": {
            "velocity_trend": "stable",  # Would be calculated from historical data
            "capacity_utilization": f"{team_velocity * 100:.0f}%",
            "burnout_risk": "low" if team_velocity < 1.0 else "medium"
        }
    }
    
    return result

async def manage_stakeholders(
    project_name: str,
    stakeholder_groups: List[str] = None,
    communication_frequency: str = "weekly",
    upcoming_decisions: List[str] = None,
    tool_context=None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Coordinate stakeholder communication and manage expectations.
    
    Args:
        project_name (str): Name of the project
        stakeholder_groups (List[str]): List of stakeholder groups involved
        communication_frequency (str): How often to communicate (daily, weekly, bi-weekly)
        upcoming_decisions (List[str]): Decisions that need stakeholder input
    
    Returns:
        Dict[str, Any]: Stakeholder management plan and communication strategy
    """
    log.info("[manage_stakeholders] called")
    
    stakeholder_groups = stakeholder_groups or ["Engineering", "Product", "Leadership"]
    upcoming_decisions = upcoming_decisions or []
    
    # Define stakeholder communication templates
    communication_templates = {
        "Engineering": {
            "focus": "Technical progress, blockers, resource needs",
            "preferred_format": "Technical standup, detailed status",
            "frequency": "Daily to weekly",
            "key_metrics": ["Velocity", "Code quality", "Technical debt"]
        },
        "Product": {
            "focus": "Feature progress, user impact, scope changes",
            "preferred_format": "Demo, user stories, metrics",
            "frequency": "Weekly to bi-weekly", 
            "key_metrics": ["Feature completion", "User feedback", "Product metrics"]
        },
        "Leadership": {
            "focus": "Timeline, budget, strategic alignment",
            "preferred_format": "Executive summary, dashboard",
            "frequency": "Weekly to monthly",
            "key_metrics": ["Budget utilization", "Timeline adherence", "ROI"]
        },
        "Customers": {
            "focus": "Benefits, timeline, impact on their workflow",
            "preferred_format": "Updates, previews, training",
            "frequency": "Milestone-based",
            "key_metrics": ["User satisfaction", "Adoption rate", "Support tickets"]
        }
    }
    
    # Generate communication plan for each group
    communication_plans = []
    for group in stakeholder_groups:
        template = communication_templates.get(group, communication_templates["Engineering"])
        
        plan = {
            "stakeholder_group": group,
            "communication_focus": template["focus"],
            "recommended_format": template["preferred_format"],
            "frequency": template["frequency"],
            "key_metrics_to_share": template["key_metrics"],
            "next_communication": get_next_communication_date(communication_frequency)
        }
        communication_plans.append(plan)
    
    # Decision management
    decision_framework = []
    for decision in upcoming_decisions:
        framework = {
            "decision": decision,
            "stakeholders_needed": determine_decision_stakeholders(decision, stakeholder_groups),
            "timeline": "1-2 weeks for consensus",
            "process": "Present options, gather input, document decision"
        }
        decision_framework.append(framework)
    
    result = {
        "status": "success",
        "project_name": project_name,
        "stakeholder_analysis": {
            "total_groups": len(stakeholder_groups),
            "communication_complexity": "high" if len(stakeholder_groups) > 4 else "medium",
            "decision_count": len(upcoming_decisions)
        },
        "communication_strategy": communication_plans,
        "decision_management": {
            "pending_decisions": decision_framework,
            "decision_process": "Consensus-driven with clear documentation",
            "escalation_path": "Program Manager → Department Head → Leadership"
        },
        "engagement_plan": {
            "regular_touchpoints": f"{communication_frequency} status updates",
            "milestone_celebrations": "End of each major phase",
            "feedback_collection": "Quarterly stakeholder surveys",
            "issue_escalation": "24-48 hour response time for blockers"
        }
    }
    
    return result

# Helper functions
def get_phase_deliverables(phase_name: str) -> List[str]:
    """Get typical deliverables for each project phase."""
    deliverables = {
        "Planning & Discovery": [
            "Project charter", "Requirements document", "Risk assessment", "Resource plan"
        ],
        "Design & Architecture": [
            "System design", "UI/UX mockups", "Technical architecture", "API specifications"
        ],
        "Development": [
            "Core features", "API implementation", "Database schema", "Unit tests"
        ],
        "Testing & QA": [
            "Test plans", "Bug fixes", "Performance testing", "Security review"
        ],
        "Deployment & Launch": [
            "Production deployment", "Monitoring setup", "Launch plan", "Post-launch review"
        ]
    }
    return deliverables.get(phase_name, ["Phase deliverables"])

def get_phase_success_criteria(phase_name: str) -> List[str]:
    """Get success criteria for each project phase."""
    criteria = {
        "Planning & Discovery": [
            "All requirements documented", "Team roles assigned", "Timeline approved"
        ],
        "Design & Architecture": [
            "Architecture review passed", "Design approved", "Technical feasibility confirmed"
        ],
        "Development": [
            "All features implemented", "Code review completed", "Unit tests passing"
        ],
        "Testing & QA": [
            "Quality gates met", "Performance targets achieved", "Security review passed"
        ],
        "Deployment & Launch": [
            "Production deployment successful", "Monitoring active", "Launch metrics met"
        ]
    }
    return criteria.get(phase_name, ["Phase objectives met"])

def assess_project_risks(duration_weeks: int, team_size: int, priority: str) -> Dict[str, Any]:
    """Assess project risks based on characteristics."""
    risks = []
    
    if duration_weeks > 26:  # > 6 months
        risks.append("Long project duration increases scope creep risk")
    if team_size < 3:
        risks.append("Small team size may limit expertise and capacity")
    if team_size > 12:
        risks.append("Large team size may create communication overhead")
    if priority == "critical":
        risks.append("High priority may lead to rushed decisions")
    
    return {
        "identified_risks": risks,
        "risk_level": "high" if len(risks) > 2 else "medium" if risks else "low",
        "mitigation_strategies": [
            "Regular stakeholder check-ins",
            "Agile development practices",
            "Clear communication channels",
            "Risk monitoring and response plans"
        ]
    }

def generate_team_roles(team_size: int) -> List[str]:
    """Generate appropriate team composition based on size."""
    base_roles = ["Tech Lead", "Developer", "Designer", "Product Manager", "QA Engineer"]
    
    if team_size <= 3:
        return base_roles[:team_size]
    elif team_size <= 8:
        return base_roles + ["DevOps Engineer", "Data Analyst"][:team_size]
    else:
        return base_roles + [
            "DevOps Engineer", "Data Analyst", "Security Engineer", 
            "Technical Writer", "Scrum Master"
        ][:team_size]

def generate_progress_recommendations(velocity_rating: str, blocker_count: int, completion: float) -> List[str]:
    """Generate recommendations based on project progress indicators."""
    recommendations = []
    
    if velocity_rating == "critical":
        recommendations.extend([
            "Immediate team capacity review needed",
            "Consider scope reduction or timeline extension",
            "Identify and address team blockers"
        ])
    elif velocity_rating == "concerning":
        recommendations.extend([
            "Review team workload and capacity",
            "Address top priority blockers",
            "Consider additional resources"
        ])
    
    if blocker_count > 3:
        recommendations.append("Focus on blocker resolution - limit new work")
    
    if completion < 25:
        recommendations.append("Review project scope and timeline expectations")
    
    return recommendations or ["Continue current approach - project on track"]

def get_next_communication_date(frequency: str) -> str:
    """Calculate next communication date based on frequency."""
    today = datetime.now()
    
    if frequency == "daily":
        next_date = today + timedelta(days=1)
    elif frequency == "weekly":
        next_date = today + timedelta(weeks=1)  
    elif frequency == "bi-weekly":
        next_date = today + timedelta(weeks=2)
    else:
        next_date = today + timedelta(weeks=1)  # default to weekly
    
    return next_date.strftime("%Y-%m-%d")

def determine_decision_stakeholders(decision: str, available_groups: List[str]) -> List[str]:
    """Determine which stakeholders need to be involved in a decision."""
    decision_lower = decision.lower()
    
    if "technical" in decision_lower or "architecture" in decision_lower:
        return [g for g in available_groups if g in ["Engineering", "Leadership"]]
    elif "feature" in decision_lower or "product" in decision_lower:
        return [g for g in available_groups if g in ["Product", "Engineering", "Customers"]]
    elif "budget" in decision_lower or "timeline" in decision_lower:
        return [g for g in available_groups if g in ["Leadership", "Product"]]
    else:
        return available_groups  # Default to all stakeholders
