# Hiring Manager tools for job descriptions and candidate screening workflows
from __future__ import annotations
from typing import Any, Dict, List, Optional
from solace_ai_connector.common.log import log

async def create_job_description(
    role_title: str,
    department: str,
    experience_level: str = "mid-level",
    required_skills: List[str] = None,
    nice_to_have_skills: List[str] = None,
    tool_context=None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Generate comprehensive job descriptions based on role requirements.
    
    Args:
        role_title (str): Job title and role name
        department (str): Department or team the role belongs to
        experience_level (str): Required experience level (entry, mid-level, senior, lead)
        required_skills (List[str]): Must-have technical and soft skills
        nice_to_have_skills (List[str]): Preferred but not required skills
    
    Returns:
        Dict[str, Any]: Complete job description with all sections
    """
    log.info("[create_job_description] called")
    
    required_skills = required_skills or []
    nice_to_have_skills = nice_to_have_skills or []
    
    # Experience level mappings
    experience_requirements = {
        "entry": {
            "years": "0-2 years",
            "responsibilities": "Learning-focused with mentorship",
            "autonomy": "Guided work with regular check-ins"
        },
        "mid-level": {
            "years": "3-5 years", 
            "responsibilities": "Independent project ownership",
            "autonomy": "Self-directed with periodic guidance"
        },
        "senior": {
            "years": "5-8 years",
            "responsibilities": "Technical leadership and mentoring",
            "autonomy": "High autonomy with strategic input"
        },
        "lead": {
            "years": "8+ years",
            "responsibilities": "Team leadership and architectural decisions",
            "autonomy": "Full autonomy with stakeholder management"
        }
    }
    
    exp_config = experience_requirements.get(experience_level, experience_requirements["mid-level"])
    
    result = {
        "status": "success",
        "job_title": role_title,
        "department": department,
        "experience_level": experience_level,
        "job_description": {
            "summary": f"We are seeking a talented {role_title} to join our {department} team.",
            "responsibilities": [
                f"Develop and maintain high-quality solutions for the {department} team",
                "Collaborate with cross-functional teams to deliver projects",
                "Participate in code reviews and technical discussions",
                "Contribute to team knowledge sharing and best practices"
            ],
            "requirements": {
                "experience": exp_config["years"],
                "required_skills": required_skills,
                "nice_to_have": nice_to_have_skills,
                "soft_skills": [
                    "Strong communication skills",
                    "Problem-solving mindset", 
                    "Team collaboration",
                    "Continuous learning attitude"
                ]
            },
            "work_environment": {
                "autonomy_level": exp_config["autonomy"],
                "team_structure": exp_config["responsibilities"],
                "growth_opportunities": "Mentoring, training, conference attendance"
            }
        },
        "compensation_guidance": {
            "salary_range": "Competitive based on experience",
            "benefits": ["Health insurance", "401k", "PTO", "Professional development"],
            "equity": "Stock options available"
        }
    }
    
    return result

async def design_screening_process(
    role_type: str,
    skills_to_assess: List[str] = None,
    interview_stages: int = 3,
    assessment_type: str = "technical",
    tool_context=None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Design comprehensive candidate screening and interview processes.
    
    Args:
        role_type (str): Type of role (engineering, design, product, etc.)
        skills_to_assess (List[str]): Key skills that need assessment
        interview_stages (int): Number of interview rounds
        assessment_type (str): Type of assessment (technical, behavioral, mixed)
    
    Returns:
        Dict[str, Any]: Complete screening process design
    """
    log.info("[design_screening_process] called")
    
    skills_to_assess = skills_to_assess or []
    
    # Role-specific assessment templates
    assessment_templates = {
        "engineering": {
            "technical_skills": ["Coding", "System Design", "Problem Solving"],
            "soft_skills": ["Communication", "Collaboration", "Learning Agility"],
            "assessments": ["Live coding", "System design", "Code review"]
        },
        "design": {
            "technical_skills": ["Design Tools", "User Research", "Prototyping"],
            "soft_skills": ["Creativity", "User Empathy", "Presentation"],
            "assessments": ["Portfolio review", "Design challenge", "User story walkthrough"]
        },
        "product": {
            "technical_skills": ["Product Strategy", "Analytics", "User Research"],
            "soft_skills": ["Leadership", "Communication", "Strategic Thinking"],
            "assessments": ["Case study", "Product strategy", "Stakeholder simulation"]
        },
        "data": {
            "technical_skills": ["Statistics", "Programming", "Data Analysis"],
            "soft_skills": ["Business Acumen", "Communication", "Critical Thinking"],
            "assessments": ["Data analysis", "SQL queries", "Business case"]
        }
    }
    
    template = assessment_templates.get(role_type, assessment_templates["engineering"])
    
    # Generate interview process
    stages = []
    stage_names = ["Initial Screening", "Technical Assessment", "Team Interview", "Final Interview", "Reference Check"]
    
    for i in range(min(interview_stages, len(stage_names))):
        stage = {
            "stage": i + 1,
            "name": stage_names[i],
            "duration": "45-60 minutes" if i > 0 else "30 minutes",
            "focus": template["technical_skills"] if i == 1 else template["soft_skills"],
            "interviewers": "Hiring manager" if i == 0 else f"{role_type} team members"
        }
        stages.append(stage)
    
    result = {
        "status": "success",
        "role_type": role_type,
        "assessment_framework": template,
        "interview_process": {
            "total_stages": interview_stages,
            "estimated_timeline": f"{interview_stages * 5-7} days",
            "stages": stages
        },
        "evaluation_criteria": {
            "technical_assessment": {
                "weight": 0.4,
                "criteria": template["technical_skills"]
            },
            "behavioral_assessment": {
                "weight": 0.3,
                "criteria": template["soft_skills"]
            },
            "cultural_fit": {
                "weight": 0.2,
                "criteria": ["Values alignment", "Team dynamics", "Growth mindset"]
            },
            "communication": {
                "weight": 0.1,
                "criteria": ["Clarity", "Active listening", "Presentation skills"]
            }
        },
        "decision_framework": {
            "scoring": "1-5 scale per criterion",
            "threshold": "3.5+ average to proceed",
            "final_decision": "Consensus-based with hiring manager approval"
        }
    }
    
    return result

async def analyze_team_needs(
    project_description: str,
    current_team_size: int = 0,
    current_skills: List[str] = None,
    project_timeline: str = "6 months",
    tool_context=None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Analyze team composition needs and role requirements for projects.
    
    Args:
        project_description (str): Description of the project or initiative
        current_team_size (int): Number of current team members
        current_skills (List[str]): Skills already present in the team
        project_timeline (str): Expected project duration
    
    Returns:
        Dict[str, Any]: Team analysis and hiring recommendations
    """
    log.info("[analyze_team_needs] called")
    
    current_skills = current_skills or []
    
    # Common skill requirements by project type
    project_skill_mapping = {
        "web_development": [
            "Frontend Development", "Backend Development", "Database Design",
            "DevOps", "UI/UX Design", "Product Management"
        ],
        "data_science": [
            "Data Analysis", "Machine Learning", "Statistics", 
            "Data Engineering", "Visualization", "Domain Expertise"
        ],
        "mobile_development": [
            "iOS Development", "Android Development", "UI/UX Design",
            "Backend APIs", "DevOps", "Product Management"
        ],
        "infrastructure": [
            "Cloud Architecture", "DevOps", "Security",
            "Monitoring", "Automation", "Site Reliability"
        ]
    }
    
    # Detect project type from description
    project_type = "web_development"  # default
    for ptype, skills in project_skill_mapping.items():
        if any(skill.lower().replace(" ", "_") in project_description.lower() for skill in skills):
            project_type = ptype
            break
    
    required_skills = project_skill_mapping[project_type]
    skill_gaps = [skill for skill in required_skills if skill not in current_skills]
    
    # Team size recommendations
    timeline_multiplier = {
        "3 months": 1.5,  # Need more people for short timeline
        "6 months": 1.0,  # Standard staffing
        "12 months": 0.8,  # Can work with smaller team
        "18+ months": 0.7   # Long-term project efficiency
    }
    
    base_team_size = len(required_skills)
    recommended_size = int(base_team_size * timeline_multiplier.get(project_timeline, 1.0))
    additional_hires = max(0, recommended_size - current_team_size)
    
    result = {
        "status": "success",
        "project_analysis": {
            "detected_type": project_type,
            "timeline": project_timeline,
            "complexity_score": len(skill_gaps) / len(required_skills)
        },
        "current_state": {
            "team_size": current_team_size,
            "existing_skills": current_skills,
            "skill_coverage": f"{len(current_skills)/len(required_skills)*100:.1f}%"
        },
        "recommendations": {
            "target_team_size": recommended_size,
            "additional_hires": additional_hires,
            "priority_skills": skill_gaps[:3],  # Top 3 most critical gaps
            "skill_gaps": skill_gaps
        },
        "hiring_plan": {
            "immediate_needs": skill_gaps[:2] if skill_gaps else [],
            "future_needs": skill_gaps[2:] if len(skill_gaps) > 2 else [],
            "hiring_timeline": f"{additional_hires * 4-6} weeks for full staffing",
            "budget_estimate": f"${additional_hires * 150000:.0f} annual salary budget"
        }
    }
    
    return result
