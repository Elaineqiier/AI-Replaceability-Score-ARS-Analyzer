import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from math import pi
import re

# Configure page settings
st.set_page_config(
    page_title="AI Replaceability Score Analyzer",
    page_icon="🤖",
    layout="wide"
)

# Constants
SCORE_DESCRIPTIONS = {
    1: "Highly Calculative - Tasks that rely primarily on logical processing, pattern recognition, and rule-based decision-making with minimal ambiguity.",
    2: "Primarily Calculative - Tasks that follow predictable patterns but occasionally require slight interpretation or contextual understanding beyond pure calculation.",
    3: "Balanced Thinking - Tasks that require equal parts analytical processing and intuitive judgment, with both structured and unstructured elements.",
    4: "Primarily Meditative - Tasks that depend mostly on nuanced human judgment, creative thinking, and emotional understanding with some analytical components.",
    5: "Highly Meditative - Tasks that fundamentally require deep human insight, complex emotional intelligence, and original thinking that transcends rule-based approaches."
}

# Job role keywords for identification
JOB_ROLES = {
    "software_developer": ["programming", "coding", "development", "software", "application", "system", "code", "developer", "engineer", "programmer"],
    "data_scientist": ["data", "analysis", "analytics", "statistics", "machine learning", "AI", "modeling", "research", "scientist", "analyst"],
    "project_manager": ["management", "planning", "coordination", "leadership", "team", "project", "schedule", "budget", "resource", "stakeholder"],
    "business_analyst": ["business", "analysis", "requirements", "process", "documentation", "specification", "improvement", "optimization", "efficiency", "workflow"],
    "designer": ["design", "creative", "visual", "art", "interface", "user experience", "UX", "UI", "graphic", "aesthetic"],
    "sales": ["sales", "selling", "marketing", "customer", "client", "revenue", "deal", "negotiation", "proposal", "pitch"],
    "teacher": ["teaching", "education", "learning", "student", "classroom", "instruction", "training", "curriculum", "academic", "school"],
    "healthcare": ["medical", "health", "patient", "care", "treatment", "clinical", "diagnosis", "therapy", "nursing", "doctor"],
    "finance": ["financial", "accounting", "banking", "investment", "trading", "risk", "audit", "budget", "finance", "money"],
    "legal": ["legal", "law", "attorney", "court", "case", "contract", "regulation", "compliance", "litigation", "justice"]
}

# Keywords for rule-based scoring
KEYWORD_SCORES = {
    1: ["calculation", "data entry", "routine", "repetitive", "automated", "structured", "data processing", 
        "predictable", "arithmetic", "formulas", "sorting", "filtering", "database", "spreadsheet", "algorithm"],
    
    2: ["basic analysis", "pattern recognition", "documentation", "report generation", "standard procedures", 
        "classification", "organized", "methodical", "verification", "monitoring", "standard customer service"],
    
    3: ["problem solving", "decision making", "moderate complexity", "collaboration", "coordination", 
        "planning", "prioritization", "content creation", "balanced", "analytical and creative", "training"],
    
    4: ["strategy", "innovation", "leadership", "negotiation", "complex analysis", "mediation", "coaching", 
        "design", "counseling", "consultation", "specialized expertise", "interpretation", "adaptation"],
    
    5: ["visionary", "crisis management", "ethical dilemma", "complex negotiation", "therapy", "deep empathy",
        "original research", "artistic creation", "philosophical thinking", "mentoring", "pioneering", "wisdom"]
}

# Dimension descriptions for scoring
DIMENSION_DESCRIPTIONS = {
    "Cognitive Complexity": {
        1: "Follows clear rules with predictable inputs and outputs",
        2: "Mostly structured with some interpretation needed",
        3: "Mix of structured and unstructured reasoning",
        4: "Primarily unstructured with complexity and ambiguity",
        5: "Highly abstract reasoning with no clear patterns"
    },
    "Creativity/Innovation": {
        1: "Follows established procedures with no variation",
        2: "Minor adaptations of existing approaches",
        3: "Combines existing ideas in new ways",
        4: "Develops substantially new approaches",
        5: "Creates completely original solutions"
    },
    "Emotional Intelligence": {
        1: "No interpersonal understanding required",
        2: "Basic awareness of others' reactions",
        3: "Moderate understanding of emotions and motivations",
        4: "Deep understanding of complex emotions",
        5: "Profound empathy and emotional wisdom"
    },
    "Adaptive Flexibility": {
        1: "Same approach works every time",
        2: "Occasional minor adjustments needed",
        3: "Regular adaptation to changing circumstances",
        4: "Constant adaptation to unique situations",
        5: "Continuous innovation in dynamic environments"
    }
}

class SimpleARSAnalyzer:
    def __init__(self):
        self.history = []
    
    def analyze_task(self, job_title: str, task_description: str) -> dict:
        """Analyze a job task using rules-based approach"""
        # Combine job title and task description for analysis
        combined_text = f"{job_title} {task_description}".lower()
        
        # Identify job role
        identified_role = self._identify_job_role(combined_text)
        
        # Count keyword matches
        score_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for score, keywords in KEYWORD_SCORES.items():
            for keyword in keywords:
                if keyword.lower() in combined_text:
                    score_counts[score] += 1
        
        # Determine overall score based on keyword matches
        if sum(score_counts.values()) > 0:
            # If we have keyword matches, weight them
            weighted_score = sum(score * count for score, count in score_counts.items()) / sum(score_counts.values())
            final_score = round(weighted_score)
        else:
            # Default to middle score if no keywords match
            final_score = 3
        
        # Calculate dimension ratings
        dimension_ratings = self._calculate_dimension_ratings(combined_text)
        
        # Generate analysis text
        analysis = self._generate_analysis(job_title, task_description, final_score, dimension_ratings, score_counts, identified_role)
        
        result = {
            "job_title": job_title,
            "task": task_description,
            "role": identified_role,
            "score": final_score,
            "analysis": analysis,
            "dimension_ratings": dimension_ratings,
            "score_description": SCORE_DESCRIPTIONS.get(final_score, "Score not found")
        }
        
        self.history.append(result)
        return result
    
    def _identify_job_role(self, text: str) -> str:
        """Identify the job role from the text"""
        max_matches = 0
        identified_role = "General"
        
        for role, keywords in JOB_ROLES.items():
            matches = sum(1 for keyword in keywords if keyword.lower() in text)
            if matches > max_matches:
                max_matches = matches
                identified_role = role.replace('_', ' ').title()
        
        return identified_role
    
    def _calculate_dimension_ratings(self, task_text: str) -> dict:
        """Calculate ratings for each dimension based on text analysis"""
        dimensions = {
            "Cognitive Complexity": 0,
            "Creativity/Innovation": 0, 
            "Emotional Intelligence": 0,
            "Adaptive Flexibility": 0
        }
        
        # Keywords for each dimension
        dimension_keywords = {
            "Cognitive Complexity": {
                1: ["simple", "routine", "basic", "straightforward", "elementary"],
                2: ["procedural", "structured", "methodical", "systematic"],
                3: ["analytical", "logical", "problem-solving", "reasoning"],
                4: ["complex", "intricate", "sophisticated", "nuanced"],
                5: ["abstract", "conceptual", "theoretical", "philosophical"]
            },
            "Creativity/Innovation": {
                1: ["follow", "adhere", "comply", "standard", "protocol"],
                2: ["adjust", "modify", "adapt", "refine"],
                3: ["develop", "improve", "enhance", "build upon"],
                4: ["create", "design", "innovate", "devise"],
                5: ["pioneer", "revolutionize", "transform", "invent"]
            },
            "Emotional Intelligence": {
                1: ["data", "information", "facts", "figures", "objective"],
                2: ["communicate", "correspond", "inform", "notify"],
                3: ["understand", "empathize", "perceive", "relate"],
                4: ["counsel", "mentor", "guide", "support"],
                5: ["heal", "transform", "inspire", "profoundly connect"]
            },
            "Adaptive Flexibility": {
                1: ["consistent", "stable", "fixed", "unchanging"],
                2: ["adjust", "accommodate", "respond", "react"],
                3: ["flexible", "versatile", "adaptable", "responsive"],
                4: ["dynamic", "evolving", "changing", "fluid"],
                5: ["transformative", "revolutionary", "groundbreaking", "disruptive"]
            }
        }
        
        # Count matches for each dimension and level
        for dimension, level_keywords in dimension_keywords.items():
            level_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            
            for level, keywords in level_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in task_text:
                        level_counts[level] += 1
            
            # Calculate weighted average if we have matches
            if sum(level_counts.values()) > 0:
                weighted_avg = sum(level * count for level, count in level_counts.items()) / sum(level_counts.values())
                dimensions[dimension] = round(weighted_avg)
            else:
                # Default to middle rating
                dimensions[dimension] = 3
        
        return dimensions
    
    def _generate_analysis(self, job_title: str, task: str, score: int, dimensions: dict, 
                         keyword_counts: dict, identified_role: str) -> str:
        """Generate analysis text based on the score and dimensions"""
        # Introduction
        analysis = f"# Analysis of Job Role and Task\n\n"
        analysis += f"**Job Title:** {job_title}\n"
        analysis += f"**Identified Role Category:** {identified_role}\n"
        analysis += f"**Task Description:** {task}\n\n"
        
        # Dimension analysis
        analysis += "## Dimension Analysis\n\n"
        for dimension, rating in dimensions.items():
            analysis += f"### {dimension}: {rating}/5\n"
            analysis += f"{DIMENSION_DESCRIPTIONS[dimension][rating]}\n\n"
        
        # Overall assessment
        analysis += "## Overall Assessment\n\n"
        analysis += f"Based on my analysis, this role and task receives an **AI Replaceability Score: {score}**.\n\n"
        analysis += f"**{SCORE_DESCRIPTIONS[score]}**\n\n"
        
        # Justification
        analysis += "### Justification\n\n"
        
        if score == 1:
            analysis += "This role and task is highly structured and rule-based, with clear inputs and outputs. "
            analysis += "It follows predictable patterns that can be fully captured by algorithms. "
            analysis += "The task requires minimal contextual understanding or emotional intelligence."
        elif score == 2:
            analysis += "This role and task follows mostly predictable patterns with occasional exceptions. "
            analysis += "While it has some structure, it occasionally requires interpretation beyond pure calculation. "
            analysis += "The task involves limited adaptation to changing circumstances."
        elif score == 3:
            analysis += "This role and task requires a balance of analytical processing and intuitive judgment. "
            analysis += "It contains both structured elements and aspects requiring human interpretation. "
            analysis += "The task involves moderate contextual understanding and adaptation."
        elif score == 4:
            analysis += "This role and task depends significantly on nuanced human judgment and creative thinking. "
            analysis += "It requires considerable emotional intelligence and contextual understanding. "
            analysis += "The task involves adapting to unique situations with substantial variation."
        elif score == 5:
            analysis += "This role and task fundamentally requires deep human insight and complex emotional intelligence. "
            analysis += "It involves original thinking that transcends rule-based approaches. "
            analysis += "The task depends on wisdom, empathy, and continuous adaptation to human needs."
        
        return analysis
    
    def get_history(self) -> list:
        """Get the analysis history"""
        return self.history

def display_radar_chart(dimensions: dict):
    """Display a radar chart for dimension ratings"""
    categories = list(dimensions.keys())
    values = list(dimensions.values())
    
    # Complete the loop for the plot
    values += values[:1]
    categories += categories[:1]
    
    # Calculate angle for each category
    angles = [n / float(len(categories)-1) * 2 * pi for n in range(len(categories))]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    # Draw the chart
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, alpha=0.25)
    
    # Set category labels
    plt.xticks(angles[:-1], categories[:-1])
    
    # Draw axis lines for each angle and label
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], color="grey", size=8)
    plt.ylim(0, 5)
    
    return fig

def create_ars_app():
    """Create and run the ARS Analyzer Streamlit app"""
    st.title("AI Replaceability Score (ARS) Analyzer")
    
    # Sidebar with information
    with st.sidebar:
        st.header("About ARS")
        st.write("The ARS Score measures where tasks fall on the calculative-to-meditative thinking spectrum.")
        
        st.subheader("Score Descriptions")
        for score, desc in SCORE_DESCRIPTIONS.items():
            st.write(f"**Score {score}:** {desc}")
            
        st.subheader("Dimensions Analyzed")
        st.write("**Cognitive Complexity**: How structured vs. unstructured is the reasoning required?")
        st.write("**Creativity/Innovation**: Does it follow established patterns or require novel approaches?")
        st.write("**Emotional Intelligence**: How much interpersonal understanding is needed?")
        st.write("**Adaptive Flexibility**: How much adaptation to changing circumstances is required?")
        
        st.subheader("Example Job Roles")
        for role in JOB_ROLES.keys():
            st.write(f"- {role.replace('_', ' ').title()}")
    
    # Initialize session state if not already done
    if "analyzer" not in st.session_state:
        st.session_state.analyzer = SimpleARSAnalyzer()
    if "history" not in st.session_state:
        st.session_state.history = []
    
    # Main content area
    st.header("Job Role and Task Analysis")
    
    # Input sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Job Role Information")
        job_title = st.text_input("Enter the job title:", 
                                 placeholder="E.g., Senior Software Developer")
        
    with col2:
        st.subheader("Task Description")
        task_description = st.text_area("Describe the specific task:", 
                                      height=150,
                                      placeholder="E.g., Develop and maintain web applications using React and Node.js")
    
    if st.button("Analyze Role and Task") and job_title and task_description:
        with st.spinner("Analyzing role and task..."):
            result = st.session_state.analyzer.analyze_task(job_title, task_description)
            st.session_state.history = st.session_state.analyzer.get_history()
        
        # Display results
        st.subheader("Analysis Results")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if result["score"]:
                st.markdown(f"### AI Replaceability Score: {result['score']}/5")
                st.markdown(f"**{result['score_description']}**")
                st.markdown("---")
                st.markdown(result["analysis"])
            else:
                st.error("Could not determine a score. Please try again with more detailed information.")
        
        with col2:
            if result["score"] and result["dimension_ratings"]:
                st.markdown("### Dimension Ratings")
                for dim, rating in result["dimension_ratings"].items():
                    st.markdown(f"**{dim}**: {rating}/5")
                
                fig = display_radar_chart(result["dimension_ratings"])
                st.pyplot(fig)
    
    # History section
    if st.session_state.history:
        st.header("Analysis History")
        for i, hist_item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Analysis {len(st.session_state.history) - i}: Score {hist_item['score']}/5"):
                st.write(f"**Job Title:** {hist_item['job_title']}")
                st.write(f"**Identified Role:** {hist_item['role']}")
                st.write(f"**Task:** {hist_item['task']}")
                st.write(f"**Score:** {hist_item['score']}/5 - {hist_item['score_description']}")
                
                # Display dimension ratings if available
                if hist_item["dimension_ratings"]:
                    st.write("**Dimension Ratings:**")
                    for dim, rating in hist_item["dimension_ratings"].items():
                        st.write(f"- {dim}: {rating}/5")
                
                st.write("**Analysis:**")
                st.write(hist_item["analysis"])

if __name__ == "__main__":
    create_ars_app()