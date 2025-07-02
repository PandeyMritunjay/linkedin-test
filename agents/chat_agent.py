import os
import json
from ai_providers import get_ai_response

class ChatAgent:
    def __init__(self):
        pass
    
    def run(self, user_input):
        if isinstance(user_input, dict):
            prompt = user_input.get("input", "")
        else:
            prompt = user_input
            
        system_prompt = """You are a helpful AI assistant specializing in LinkedIn optimization, career advice, and job search strategies. 
Provide clear, actionable advice and answer questions about:
- LinkedIn profile optimization
- Career development
- Job search strategies
- Professional networking
- Industry insights

Be conversational, helpful, and provide specific, practical guidance."""
        
        try:
            response = get_ai_response(prompt, system_prompt)
            return response
        except Exception as e:
            return f"I apologize, but I'm currently unable to respond due to technical issues. Please try again later. Error: {str(e)}" 