import os
import json
from ai_providers import get_ai_response

class ContentOptimizationAgent:
    def __init__(self):
        pass
    
    def run(self, user_input):
        if isinstance(user_input, dict):
            prompt = user_input.get("input", "")
        else:
            prompt = user_input
            
        system_prompt = """You are an expert Content Optimizer for LinkedIn profiles. Rewrite the given content to:
1. Improve clarity and impact
2. Add relevant keywords
3. Make it more professional and engaging
4. Optimize for ATS (Applicant Tracking Systems)
5. Provide alternative versions

Format your response with the original content, optimized version, key improvements, and alternative suggestions."""
        
        try:
            response = get_ai_response(prompt, system_prompt)
            return response
        except Exception as e:
            return f"I apologize, but I'm currently unable to optimize content due to technical issues. Please try again later. Error: {str(e)}" 