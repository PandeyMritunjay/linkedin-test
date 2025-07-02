import os
import json
from ai_providers import get_ai_response

class JobFitAgent:
    def __init__(self):
        pass
    
    def run(self, user_input):
        if isinstance(user_input, dict):
            prompt = user_input.get("input", "")
        else:
            prompt = user_input
            
        system_prompt = """You are an expert Job Fit Analyzer. Analyze the job description and provide:
1. Overall fit score (0-100)
2. Skill match percentage
3. Experience match percentage
4. Education match percentage
5. Competitive advantages
6. Missing skills to develop
7. Application strategy tips
8. Improvement recommendations

Format your response as a comprehensive job fit analysis."""
        
        try:
            response = get_ai_response(prompt, system_prompt)
            return response
        except Exception as e:
            return f"I apologize, but I'm currently unable to analyze job fit due to technical issues. Please try again later. Error: {str(e)}" 