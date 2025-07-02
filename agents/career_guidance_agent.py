import os
import json
from ai_providers import get_ai_response

class CareerGuidanceAgent:
    def __init__(self):
        pass
    
    def run(self, user_input):
        if isinstance(user_input, dict):
            prompt = user_input.get("input", "")
        else:
            prompt = user_input
            
        system_prompt = """You are an expert Career Guidance Advisor. Provide personalized career guidance including:
1. Growth opportunities and career paths
2. Learning resources and certifications
3. Networking strategies and events
4. Market trends and industry insights
5. Skill development recommendations
6. Actionable next steps

Format your response with clear sections for each area of guidance."""
        
        try:
            response = get_ai_response(prompt, system_prompt)
            return response
        except Exception as e:
            return f"I apologize, but I'm currently unable to provide career guidance due to technical issues. Please try again later. Error: {str(e)}" 