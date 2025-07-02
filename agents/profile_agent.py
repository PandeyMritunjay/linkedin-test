import os
import json
from ai_providers import get_ai_response

class ProfileAnalysisAgent:
    def __init__(self):
        pass
    
    def run(self, user_input):
        if isinstance(user_input, dict):
            prompt = user_input.get("input", "")
        else:
            prompt = user_input
            
        system_prompt = """You are an expert LinkedIn Profile Optimizer. Analyze the given LinkedIn profile and provide:
1. Overall score (0-100)
2. Profile completeness percentage
3. Section-by-section scores (headline, summary, experience, education, skills)
4. Key strengths (3-5 points)
5. Areas for improvement (3-5 points)
6. Recommended keywords
7. Detailed recommendations with step-by-step actions

Format your response as a comprehensive analysis with clear sections."""
        
        def parse_analysis_response(response):
            import re
            result = {}
            # Overall Score
            match = re.search(r"Overall Score\s*[:\-]?\s*(\d+)", response, re.I)
            if match:
                result["overall_score"] = int(match.group(1))
            # Profile Completeness
            match = re.search(r"Profile Completeness(?: Percentage)?\s*[:\-]?\s*(\d+)%", response, re.I)
            if match:
                result["profile_completeness"] = int(match.group(1))
            # Section Scores
            section_scores = {}
            section = re.search(r"Section[- ]?by[- ]?Section Scores[:\-]?(.*?)(?:Key Strengths|Areas for Improvement|Recommended Keywords|Detailed Recommendations|$)", response, re.S|re.I)
            if section:
                text = section.group(1)
                for key in ["headline", "summary", "experience", "education", "skills"]:
                    m = re.search(rf"{key.capitalize()}[\s:]*([\d/]+)[^\d]*(\([^)]+\))?", text, re.I)
                    if m:
                        score = m.group(1)
                        section_scores[key] = score
            result["section_scores"] = section_scores
            # Strengths
            strengths = re.findall(r"Key Strengths[:\-]?\s*(?:\n|\r|\r\n)?((?:\d+\. .+\n?)+)", response, re.I)
            if strengths:
                items = re.findall(r"\d+\.\s*(.+)", strengths[0])
                result["strengths"] = items
            else:
                result["strengths"] = []
            # Weaknesses
            weaknesses = re.findall(r"Areas for Improvement[:\-]?\s*(?:\n|\r|\r\n)?((?:\d+\. .+\n?)+)", response, re.I)
            if weaknesses:
                items = re.findall(r"\d+\.\s*(.+)", weaknesses[0])
                result["weaknesses"] = items
            else:
                result["weaknesses"] = []
            # Keywords
            keywords = re.findall(r"Recommended Keywords[:\-]?\s*(.+)", response, re.I)
            if keywords:
                result["keywords"] = [k.strip() for k in re.split(r",|\n", keywords[0]) if k.strip()]
            else:
                result["keywords"] = []
            # Recommendations
            recs = re.findall(r"Detailed Recommendations(?: with Step[- ]by[- ]Step Actions)?[:\-]?\s*((?:\d+\. .+\n?)+)", response, re.I)
            if recs:
                items = re.findall(r"\d+\.\s*(.+)", recs[0])
                result["recommendations"] = items
            else:
                result["recommendations"] = []
            return result
        try:
            response = get_ai_response(prompt, system_prompt)
            # Try to parse the response
            parsed = parse_analysis_response(response)
            # If parsing yields at least section_scores or strengths, return dict, else fallback
            if parsed.get("section_scores") or parsed.get("strengths"):
                return parsed
            return response
        except Exception as e:
            return f"I apologize, but I'm currently unable to analyze LinkedIn profiles due to technical issues. Please try again later. Error: {str(e)}" 