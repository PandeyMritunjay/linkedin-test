
import logging
from typing import Dict, Any, List, Optional
from ai_providers import get_ai_response
from config import AppConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinkedInOptimizerAgent:
    """Comprehensive LinkedIn Profile Optimizer Agent"""
    
    def __init__(self):
        """Initialize the LinkedIn optimizer agent"""
        self.system_prompt = AppConfig.AGENT_CONFIG["system_prompt"]
        logger.info("LinkedIn Optimizer Agent initialized")
    
    def analyze_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive profile analysis with scoring and recommendations
        
        Args:
            profile_data: LinkedIn profile data
            
        Returns:
            Analysis results with scores and recommendations
        """
        try:
            logger.info("Analyzing LinkedIn profile...")
            
            prompt = f"""
            Please analyze this LinkedIn profile comprehensively and provide detailed feedback in the EXACT format specified:

            PROFILE DATA:
            Name: {profile_data.get('name', 'N/A')}
            Headline: {profile_data.get('headline', 'N/A')}
            Location: {profile_data.get('location', 'N/A')}
            Industry: {profile_data.get('industry', 'N/A')}
            Summary: {profile_data.get('summary', 'N/A')}
            
            Experience ({len(profile_data.get('experience', []))} positions):
            {self._format_experience(profile_data.get('experience', []))}
            
            Education ({len(profile_data.get('education', []))} entries):
            {self._format_education(profile_data.get('education', []))}
            
            Skills ({len(profile_data.get('skills', []))} listed):
            {', '.join(profile_data.get('skills', [])[:15])}{'...' if len(profile_data.get('skills', [])) > 15 else ''}
            
            Connections: {profile_data.get('connections', 0)}
            
            REQUIRED FORMAT - Please follow this EXACT structure and provide DETAILED analysis:

            OVERALL SCORE: [0-100 number]

            SECTION SCORES:
            - Headline: [0-100 number]
            - Summary: [0-100 number]  
            - Experience: [0-100 number]
            - Education: [0-100 number]
            - Skills: [0-100 number]

            STRENGTHS:
            - [Detailed strength 1 with specific examples and impact]
            - [Detailed strength 2 with specific examples and impact]
            - [Detailed strength 3 with specific examples and impact]
            - [Detailed strength 4 with specific examples and impact]
            - [Detailed strength 5 with specific examples and impact]
            - [Detailed strength 6 with specific examples and impact]

            WEAKNESSES:
            - [Detailed weakness 1 with specific areas for improvement and why it matters]
            - [Detailed weakness 2 with specific areas for improvement and why it matters]
            - [Detailed weakness 3 with specific areas for improvement and why it matters]
            - [Detailed weakness 4 with specific areas for improvement and why it matters]
            - [Detailed weakness 5 with specific areas for improvement and why it matters]

            RECOMMENDATIONS:
            - [Detailed actionable recommendation 1 with step-by-step guidance and expected impact]
            - [Detailed actionable recommendation 2 with step-by-step guidance and expected impact]
            - [Detailed actionable recommendation 3 with step-by-step guidance and expected impact]
            - [Detailed actionable recommendation 4 with step-by-step guidance and expected impact]
            - [Detailed actionable recommendation 5 with step-by-step guidance and expected impact]
            - [Detailed actionable recommendation 6 with step-by-step guidance and expected impact]
            - [Detailed actionable recommendation 7 with step-by-step guidance and expected impact]
            - [Detailed actionable recommendation 8 with step-by-step guidance and expected impact]

            KEYWORDS:
            - [Industry-specific keyword 1 with explanation of relevance]
            - [Industry-specific keyword 2 with explanation of relevance]
            - [Industry-specific keyword 3 with explanation of relevance]
            - [Industry-specific keyword 4 with explanation of relevance]
            - [Industry-specific keyword 5 with explanation of relevance]
            - [Industry-specific keyword 6 with explanation of relevance]

            Please provide comprehensive, specific, and actionable insights based on the actual profile data. 
            Include detailed explanations for each point, specific examples where possible, and quantifiable improvements.
            """
            
            response = get_ai_response(prompt, self.system_prompt)
            logger.info(f"AI Response received (length: {len(response)})")
            logger.debug(f"Full AI Response: {response[:500]}...")
            
            # Parse and structure the response
            analysis = self._parse_analysis_response(response, profile_data)
            
            # Validate that we got meaningful content
            if not analysis.get('strengths') or analysis['strengths'] == ["Analysis available in detailed feedback"]:
                logger.warning("Parsing failed, using enhanced fallback")
                return self._get_enhanced_fallback_analysis(profile_data, response)
            
            logger.info("Profile analysis completed successfully")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing profile: {e}")
            return self._get_enhanced_fallback_analysis(profile_data)
    
    def analyze_job_fit(self, profile_data: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """
        Analyze how well the profile fits a specific job
        
        Args:
            profile_data: LinkedIn profile data
            job_description: Target job description
            
        Returns:
            Job fit analysis with score and recommendations
        """
        try:
            logger.info("Analyzing job fit...")
            
            prompt = f"""
            Analyze how well this LinkedIn profile matches the given job description:

            LINKEDIN PROFILE:
            Name: {profile_data.get('name', 'N/A')}
            Headline: {profile_data.get('headline', 'N/A')}
            Summary: {profile_data.get('summary', 'N/A')}
            
            Experience:
            {self._format_experience(profile_data.get('experience', []))}
            
            Skills: {', '.join(profile_data.get('skills', []))}
            
            Education:
            {self._format_education(profile_data.get('education', []))}

            JOB DESCRIPTION:
            {job_description}

            REQUIRED FORMAT - Please follow this EXACT structure:

            OVERALL FIT SCORE: [0-100 number]

            SKILL MATCH: [0-100 number]

            EXPERIENCE MATCH: [0-100 number]

            EDUCATION MATCH: [0-100 number]

            MISSING SKILLS:
            - [Detailed missing skill 1 with explanation of importance and how to acquire it]
            - [Detailed missing skill 2 with explanation of importance and how to acquire it]
            - [Detailed missing skill 3 with explanation of importance and how to acquire it]
            - [Detailed missing skill 4 with explanation of importance and how to acquire it]
            - [Detailed missing skill 5 with explanation of importance and how to acquire it]

            COMPETITIVE ADVANTAGES:
            - [Detailed advantage 1 with specific examples and how it differentiates the candidate]
            - [Detailed advantage 2 with specific examples and how it differentiates the candidate]
            - [Detailed advantage 3 with specific examples and how it differentiates the candidate]
            - [Detailed advantage 4 with specific examples and how it differentiates the candidate]
            - [Detailed advantage 5 with specific examples and how it differentiates the candidate]

            IMPROVEMENT RECOMMENDATIONS:
            - [Detailed recommendation 1 with step-by-step implementation and timeline]
            - [Detailed recommendation 2 with step-by-step implementation and timeline]
            - [Detailed recommendation 3 with step-by-step implementation and timeline]
            - [Detailed recommendation 4 with step-by-step implementation and timeline]
            - [Detailed recommendation 5 with step-by-step implementation and timeline]
            - [Detailed recommendation 6 with step-by-step implementation and timeline]

            APPLICATION TIPS:
            - [Detailed application tip 1 with specific examples and expected outcomes]
            - [Detailed application tip 2 with specific examples and expected outcomes]
            - [Detailed application tip 3 with specific examples and expected outcomes]
            - [Detailed application tip 4 with specific examples and expected outcomes]
            - [Detailed application tip 5 with specific examples and expected outcomes]
            - [Detailed application tip 6 with specific examples and expected outcomes]

            Provide comprehensive, specific, and actionable feedback based on the job requirements.
            Include detailed explanations, quantifiable improvements, and practical implementation steps.
            """
            
            response = get_ai_response(prompt, self.system_prompt)
            
            # Parse and structure the response
            job_fit = self._parse_job_fit_response(response, profile_data, job_description)
            
            logger.info("Job fit analysis completed")
            return job_fit
            
        except Exception as e:
            logger.error(f"Error analyzing job fit: {e}")
            return self._get_fallback_job_fit()
    
    def optimize_content(self, profile_data: Dict[str, Any], section: str, target_role: str = "") -> Dict[str, Any]:
        """
        Optimize specific profile sections for better impact
        
        Args:
            profile_data: LinkedIn profile data
            section: Section to optimize (headline, summary, experience)
            target_role: Target role for optimization (optional)
            
        Returns:
            Optimized content suggestions
        """
        try:
            logger.info(f"Optimizing {section} content...")
            
            current_content = self._get_section_content(profile_data, section)
            
            prompt = f"""
            Optimize this LinkedIn profile {section} for maximum impact:

            CURRENT {section.upper()}:
            {current_content}

            PROFILE CONTEXT:
            Name: {profile_data.get('name', 'N/A')}
            Industry: {profile_data.get('industry', 'N/A')}
            Experience Level: {self._assess_experience_level(profile_data)}
            Key Skills: {', '.join(profile_data.get('skills', [])[:10])}
            {"Target Role: " + target_role if target_role else ""}

            REQUIRED FORMAT - Please follow this EXACT structure:

            OPTIMIZED {section.upper()}:
            [Your improved version of the {section} here - write the complete optimized text]

            KEY IMPROVEMENTS:
            - [Specific improvement 1 with explanation]
            - [Specific improvement 2 with explanation]
            - [Specific improvement 3 with explanation]
            - [Specific improvement 4 with explanation]

            KEYWORDS ADDED:
            - [Important keyword 1]
            - [Important keyword 2]
            - [Important keyword 3]
            - [Important keyword 4]

            ALTERNATIVE VERSIONS:
            Version 1: [Alternative version 1]
            Version 2: [Alternative version 2]

            Make it compelling, professional, and ATS-optimized.
            """
            
            response = get_ai_response(prompt, self.system_prompt)
            
            # Parse and structure the response
            optimization = self._parse_optimization_response(response, section, current_content)
            
            logger.info("Content optimization completed")
            return optimization
            
        except Exception as e:
            logger.error(f"Error optimizing content: {e}")
            return self._get_fallback_optimization(section)
    
    def provide_career_guidance(self, profile_data: Dict[str, Any], career_goals: str = "") -> Dict[str, Any]:
        """
        Provide comprehensive career guidance and development recommendations
        
        Args:
            profile_data: LinkedIn profile data
            career_goals: User's career goals (optional)
            
        Returns:
            Career guidance and development plan
        """
        try:
            logger.info("Generating career guidance...")
            
            prompt = f"""
            Provide comprehensive career guidance for this professional:

            CURRENT PROFILE:
            Name: {profile_data.get('name', 'N/A')}
            Headline: {profile_data.get('headline', 'N/A')}
            Industry: {profile_data.get('industry', 'N/A')}
            Experience Level: {self._assess_experience_level(profile_data)}
            
            Recent Experience:
            {self._format_recent_experience(profile_data.get('experience', []))}
            
            Skills: {', '.join(profile_data.get('skills', []))}
            Education: {self._format_education(profile_data.get('education', []))}
            
            {"Career Goals: " + career_goals if career_goals else ""}

            REQUIRED FORMAT - Please follow this EXACT structure:

            GROWTH OPPORTUNITIES:
            - [Detailed career opportunity 1 with market demand analysis and salary expectations]
            - [Detailed career opportunity 2 with market demand analysis and salary expectations]
            - [Detailed career opportunity 3 with market demand analysis and salary expectations]
            - [Detailed career opportunity 4 with market demand analysis and salary expectations]
            - [Detailed career opportunity 5 with market demand analysis and salary expectations]

            PRIORITY SKILLS TO DEVELOP:
            - [Critical skill 1 with detailed explanation, learning timeline, and career impact]
            - [Critical skill 2 with detailed explanation, learning timeline, and career impact]
            - [Critical skill 3 with detailed explanation, learning timeline, and career impact]
            - [Critical skill 4 with detailed explanation, learning timeline, and career impact]
            - [Critical skill 5 with detailed explanation, learning timeline, and career impact]
            - [Critical skill 6 with detailed explanation, learning timeline, and career impact]

            LEARNING RESOURCES:
            - [Specific course/certification 1 with provider, duration, cost, and career value]
            - [Specific course/certification 2 with provider, duration, cost, and career value]
            - [Specific course/certification 3 with provider, duration, cost, and career value]
            - [Specific course/certification 4 with provider, duration, cost, and career value]
            - [Specific course/certification 5 with provider, duration, cost, and career value]

            NETWORKING STRATEGY:
            - [Detailed networking action 1 with specific platforms, events, and expected outcomes]
            - [Detailed networking action 2 with specific platforms, events, and expected outcomes]
            - [Detailed networking action 3 with specific platforms, events, and expected outcomes]
            - [Detailed networking action 4 with specific platforms, events, and expected outcomes]
            - [Detailed networking action 5 with specific platforms, events, and expected outcomes]

            MARKET TRENDS:
            - [Detailed industry trend 1 with impact analysis and how to leverage it]
            - [Detailed industry trend 2 with impact analysis and how to leverage it]
            - [Detailed industry trend 3 with impact analysis and how to leverage it]
            - [Detailed industry trend 4 with impact analysis and how to leverage it]
            - [Detailed industry trend 5 with impact analysis and how to leverage it]

            ACTION PLAN:
            - [Immediate action 1 (next 30 days) with specific steps and success metrics]
            - [Immediate action 2 (next 30 days) with specific steps and success metrics]
            - [Short-term action 3 (next 3 months) with specific steps and success metrics]
            - [Short-term action 4 (next 3 months) with specific steps and success metrics]
            - [Medium-term action 5 (next 6 months) with specific steps and success metrics]
            - [Medium-term action 6 (next 6 months) with specific steps and success metrics]
            - [Long-term action 7 (next 12 months) with specific steps and success metrics]
            - [Long-term action 8 (next 12 months) with specific steps and success metrics]

            Provide comprehensive, actionable, and personalized advice based on the profile data.
            Include detailed explanations, specific timelines, quantifiable goals, and measurable outcomes.
            """
            
            response = get_ai_response(prompt, self.system_prompt)
            
            # Parse and structure the response
            guidance = self._parse_career_guidance_response(response, profile_data)
            
            logger.info("Career guidance generated")
            return guidance
            
        except Exception as e:
            logger.error(f"Error generating career guidance: {e}")
            return self._get_fallback_career_guidance()
    
    def chat_response(self, message: str, profile_data: Optional[Dict[str, Any]] = None, context: Optional[List[Dict]] = None) -> str:
        """
        Handle conversational interactions about LinkedIn optimization
        
        Args:
            message: User message
            profile_data: LinkedIn profile data (optional)
            context: Previous conversation context (optional)
            
        Returns:
            AI response to user message
        """
        try:
            logger.info("Generating chat response...")
            
            # Build context prompt
            context_info = ""
            if profile_data:
                context_info = f"""
                PROFILE CONTEXT:
                Name: {profile_data.get('name', 'N/A')}
                Headline: {profile_data.get('headline', 'N/A')}
                Industry: {profile_data.get('industry', 'N/A')}
                Experience Level: {self._assess_experience_level(profile_data)}
                """
            
            # Add conversation history
            conversation_history = ""
            if context:
                conversation_history = "\nCONVERSATION HISTORY:\n"
                for msg in context[-3:]:  # Last 3 messages for context
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    conversation_history += f"{role.title()}: {content}\n"
            
            prompt = f"""
            {context_info}
            {conversation_history}
            
            USER MESSAGE: {message}
            
            Provide a helpful, professional response about LinkedIn optimization, career development, or job search strategies. 
            Be conversational but informative, and offer specific actionable advice when possible.
            """
            
            response = get_ai_response(prompt, self.system_prompt)
            
            logger.info("Chat response generated")
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try rephrasing your question or try again later."
    
    # Helper methods
    def _format_experience(self, experience: List[Dict]) -> str:
        """Format experience data for prompts"""
        if not experience:
            return "No experience listed"
        
        formatted = []
        for exp in experience[:3]:  # Top 3 most recent
            title = exp.get('title', 'N/A')
            company = exp.get('company', 'N/A')
            duration = exp.get('duration', 'N/A')
            description = exp.get('description', 'No description')[:200] + "..." if len(exp.get('description', '')) > 200 else exp.get('description', 'No description')
            formatted.append(f"• {title} at {company} ({duration})\n  {description}")
        
        return "\n".join(formatted)
    
    def _format_education(self, education: List[Dict]) -> str:
        """Format education data for prompts"""
        if not education:
            return "No education listed"
        
        formatted = []
        for edu in education:
            school = edu.get('school', 'N/A')
            degree = edu.get('degree', 'N/A')
            duration = edu.get('duration', 'N/A')
            formatted.append(f"• {degree} from {school} ({duration})")
        
        return "\n".join(formatted)
    
    def _format_recent_experience(self, experience: List[Dict]) -> str:
        """Format most recent experience"""
        if not experience:
            return "No experience listed"
        
        recent = experience[0] if experience else {}
        title = recent.get('title', 'N/A')
        company = recent.get('company', 'N/A')
        duration = recent.get('duration', 'N/A')
        description = recent.get('description', 'No description')[:300] + "..." if len(recent.get('description', '')) > 300 else recent.get('description', 'No description')
        
        return f"{title} at {company} ({duration})\n{description}"
    
    def _assess_experience_level(self, profile_data: Dict[str, Any]) -> str:
        """Assess experience level based on profile"""
        experience = profile_data.get('experience', [])
        if not experience:
            return "Entry Level"
        
        total_years = len(experience) * 1.5  # Rough estimate
        if total_years < 2:
            return "Entry Level"
        elif total_years < 5:
            return "Mid Level"
        elif total_years < 10:
            return "Senior Level"
        else:
            return "Executive Level"
    
    def _get_section_content(self, profile_data: Dict[str, Any], section: str) -> str:
        """Get content for specific profile section"""
        if section == "headline":
            return profile_data.get('headline', 'No headline')
        elif section == "summary":
            return profile_data.get('summary', 'No summary')
        elif section == "experience":
            return self._format_experience(profile_data.get('experience', []))
        else:
            return "Section not found"
    
    def _parse_analysis_response(self, response: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI response into structured analysis"""
        return {
            "overall_score": self._extract_score(response, "overall"),
            "section_scores": {
                "headline": self._extract_score(response, "headline"),
                "summary": self._extract_score(response, "summary"),
                "experience": self._extract_score(response, "experience"),
                "education": self._extract_score(response, "education"),
                "skills": self._extract_score(response, "skills")
            },
            "strengths": self._extract_list_items(response, "strengths"),
            "weaknesses": self._extract_list_items(response, "weaknesses"),
            "recommendations": self._extract_list_items(response, "recommendations"),
            "keywords": self._extract_list_items(response, "keywords"),
            "detailed_feedback": response,
            "profile_completeness": self._calculate_completeness(profile_data)
        }
    
    def _parse_job_fit_response(self, response: str, profile_data: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """Parse job fit analysis response"""
        return {
            "fit_score": self._extract_score(response, "fit"),
            "skill_match": self._extract_score(response, "skill"),
            "experience_match": self._extract_score(response, "experience"),
            "education_match": self._extract_score(response, "education"),
            "missing_skills": self._extract_list_items(response, "missing skills"),
            "advantages": self._extract_list_items(response, "competitive advantages"),
            "recommendations": self._extract_list_items(response, "improvement recommendations"),
            "application_tips": self._extract_list_items(response, "application tips"),
            "detailed_analysis": response
        }
    
    def _parse_optimization_response(self, response: str, section: str, original: str) -> Dict[str, Any]:
        """Parse content optimization response"""
        return {
            "section": section,
            "original_content": original,
            "optimized_content": self._extract_optimized_content(response),
            "improvements": self._extract_list_items(response, "key improvements"),
            "keywords_added": self._extract_list_items(response, "keywords added"),
            "alternatives": self._extract_alternatives(response),
            "detailed_explanation": response
        }
    
    def _parse_career_guidance_response(self, response: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse career guidance response"""
        return {
            "career_stage": self._assess_experience_level(profile_data),
            "growth_opportunities": self._extract_list_items(response, "growth opportunities"),
            "skill_priorities": self._extract_list_items(response, "priority skills"),
            "learning_resources": self._extract_list_items(response, "learning resources"),
            "networking_strategy": self._extract_list_items(response, "networking strategy"),
            "market_trends": self._extract_list_items(response, "market trends"),
            "action_plan": self._extract_list_items(response, "action plan"),
            "detailed_guidance": response
        }
    
    def _extract_score(self, text: str, keyword: str) -> int:
        """Extract numerical score from text"""
        import re
        patterns = [
            rf"{keyword}.*?(\d+)/100",
            rf"{keyword}.*?(\d+)%",
            rf"{keyword}.*?score.*?(\d+)",
            rf"(\d+).*?{keyword}"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                return min(max(score, 0), 100)  # Clamp between 0-100
        
        return 75
    
    def _extract_list_items(self, text: str, keyword: str) -> List[str]:
        """Extract list items from text with comprehensive pattern matching"""
        import re
        
        logger.info(f"Extracting items for keyword: {keyword}")
        
        keyword_variations = [
            keyword.lower(),
            keyword.lower().replace('_', ' '),
            keyword.lower().replace('_', ''),
            keyword.upper(),
            keyword.capitalize(),
            keyword.title()
        ]
        
        # Add specific variations for common keywords
        if keyword.lower() == 'application':
            keyword_variations.extend(['application tips', 'tips', 'application strategy'])
        elif keyword.lower() == 'improvements':
            keyword_variations.extend(['key improvements', 'improvements made', 'changes'])
        elif keyword.lower() == 'networking':
            keyword_variations.extend(['networking strategy', 'network building', 'professional network'])
        elif keyword.lower() == 'opportunities':
            keyword_variations.extend(['growth opportunities', 'career opportunities', 'next career moves'])
        elif keyword.lower() == 'resources':
            keyword_variations.extend(['learning resources', 'courses', 'certifications', 'training'])
        elif keyword.lower() == 'action':
            keyword_variations.extend(['action plan', 'roadmap', 'next steps', 'recommendations'])
        
        section_patterns = []
        for var in keyword_variations:
            section_patterns.extend([
                # Pattern 1: Section header followed by ** and then content
                rf"{re.escape(var)}[:\s]*\n?\*\*\n?(.*?)(?=\n\n|\n[A-Z][A-Z\s]*:|\n\d+\.|$)",
                # Pattern 2: Section header with content directly after
                rf"{re.escape(var)}[:\s]*\n?((?:(?!\n\n|\n[A-Z][A-Z\s]*:).)*)",
                # Pattern 3: Section header in bold
                rf"\*\*{re.escape(var)}\*\*[:\s]*\n?(.*?)(?=\n\n|\n\*\*[A-Z]|\n\d+\.|$)",
                # Pattern 4: Section header with markdown
                rf"#{1,3}\s*{re.escape(var)}[:\s]*\n?(.*?)(?=\n\n|\n#{1,3}|\n\d+\.|$)",
                # Pattern 5: Section header at start of line
                rf"^{re.escape(var)}[:\s]*\n?((?:(?!\n\n|\n[A-Z][A-Z\s]*:).)*)",
                # Pattern 6: Numbered section
                rf"^\d+\.\s*{re.escape(var)}[:\s]*\n?(.*?)(?=\n\n|\n\d+\.|\n[A-Z]|$)"
            ])
        
        section_text = ""
        matched_pattern = ""
        
        for pattern in section_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL | re.MULTILINE)
            if match:
                section_text = match.group(1).strip()
                matched_pattern = pattern
                logger.info(f"Found section for {keyword} using pattern: {matched_pattern[:50]}...")
                logger.info(f"Section content: {section_text[:150]}...")
                logger.info(f"Full section content: {repr(section_text)}")
                break
        
        if not section_text:
            logger.warning(f"No section found for keyword: {keyword}, trying broader search...")
            

            lines = text.split('\n')
            for i, line in enumerate(lines):
                if any(var in line.lower() for var in keyword_variations):
                    # Found keyword, collect following lines
                    section_lines = []
                    start_collecting = False
                    
                    # Check if the next line is just ** (common AI formatting)
                    if i + 1 < len(lines) and lines[i + 1].strip() == '**':
                        start_collecting = True
                        start_idx = i + 2  # Skip the ** line
                    else:
                        start_collecting = True
                        start_idx = i + 1
                    
                    if start_collecting:
                        for j in range(start_idx, min(start_idx + 20, len(lines))):  # Look ahead 20 lines max
                            if j >= len(lines):
                                break
                            next_line = lines[j].strip()
                            if not next_line:
                                continue
                            # Stop if we hit another major section
                            if (re.match(r'^[A-Z][A-Z\s]*:$', next_line) or 
                                re.match(r'^\*\*[A-Z]', next_line) or
                                next_line.isupper()):
                                break
                            section_lines.append(next_line)
                    
                    if section_lines:
                        section_text = '\n'.join(section_lines)
                        logger.info(f"Found content using broader search: {section_text[:100]}...")
                        break
        
        # Extract items from the section text
        items = []
        if section_text:
            # Enhanced item extraction patterns
            item_patterns = [
                r'^\s*[•\-\*]\s*(.+)',  # Bullet points
                r'^\s*\d+\.\s*(.+)',    # Numbered lists
                r'^\s*-\s*(.+)',        # Dash lists
                r'^\s*\*\s*(.+)',       # Asterisk lists
                r'^\s*→\s*(.+)',        # Arrow lists
                r'^\s*▪\s*(.+)',        # Square bullet
                r'^\s*◦\s*(.+)',        # Circle bullet
            ]
            
            lines = section_text.split('\n')
            for line in lines:
                line = line.strip()
                if not line or len(line) < 3:
                    continue
                
                # Try each pattern
                item_found = False
                for pattern in item_patterns:
                    match = re.match(pattern, line)
                    if match:
                        item_content = match.group(1).strip()
                        if len(item_content) > 5:  # Only substantial content
                            items.append(item_content)
                            item_found = True
                            break
                
                # If no pattern matched but it's a substantial line, include it
                if not item_found and len(line) > 10:
                    # Skip if it looks like a section header
                    if not (re.match(r'^[A-Z][A-Z\s]*:$', line) or 
                           line.startswith('**') and line.endswith('**')):
                        items.append(line)
        
        # Clean up and format items
        cleaned_items = []
        for item in items:
            # Remove markdown formatting
            cleaned_item = re.sub(r'\*\*(.*?)\*\*', r'\1', item)  # **bold** → bold
            cleaned_item = re.sub(r'\*(.*?)\*', r'\1', cleaned_item)  # *italic* → italic
            
            # Remove extra symbols and clean up
            cleaned_item = cleaned_item.strip(' -•*:→▪◦')
            
            # Remove trailing colons
            if cleaned_item.endswith(':'):
                cleaned_item = cleaned_item[:-1].strip()
            
            # Only add substantial content
            if len(cleaned_item) > 8 and not cleaned_item.lower().startswith('detailed'):
                cleaned_items.append(cleaned_item)
        
        if cleaned_items:
            logger.info(f"Extracted {len(cleaned_items)} items for {keyword}")
            return cleaned_items[:10]  # Limit to top 10 items
        else:
            logger.warning(f"No items extracted for {keyword}, using enhanced fallback")
            return self._get_fallback_items(keyword, text)
    
    def _get_fallback_items(self, keyword: str, full_text: str) -> List[str]:
        """Generate contextual fallback items based on keyword and available text"""
        fallback_items = {
            'application': [
                "Tailor your resume to highlight relevant skills and experience",
                "Write a compelling cover letter that addresses the job requirements",
                "Prepare specific examples that demonstrate your qualifications",
                "Research the company culture and values before applying"
            ],
            'improvements': [
                "Enhanced keyword optimization for better visibility",
                "Improved professional language and impact statements",
                "Better structure and formatting for readability",
                "Added quantifiable achievements and metrics"
            ],
            'networking': [
                "Connect with industry professionals and thought leaders",
                "Engage with relevant LinkedIn groups and discussions",
                "Attend virtual and in-person networking events",
                "Share valuable content to establish thought leadership"
            ],
            'opportunities': [
                "Senior-level positions in your current field",
                "Leadership and management roles",
                "Specialized consulting opportunities",
                "Cross-functional project leadership positions"
            ],
            'resources': [
                "Industry-specific online courses and certifications",
                "Professional development workshops and seminars",
                "Relevant books and publications in your field",
                "Mentorship programs and coaching opportunities"
            ],
            'action': [
                "Update your LinkedIn profile with recent achievements",
                "Expand your professional network strategically",
                "Develop priority skills identified in your analysis",
                "Set up informational interviews with industry contacts"
            ]
        }
        
        return fallback_items.get(keyword.lower(), [
            f"Detailed {keyword} recommendations available in the comprehensive analysis",
            f"Personalized {keyword} guidance based on your profile strengths",
            f"Strategic {keyword} planning to advance your career goals"
        ])
    
    def _extract_optimized_content(self, text: str) -> str:
        """Extract optimized content from response with multiple patterns"""
        import re
        
        logger.info("Extracting optimized content...")
        
        # Comprehensive patterns for optimized content
        patterns = [
            r"OPTIMIZED\s+\w+[:\s]*\n?(.*?)(?=\n\n|\nKEY IMPROVEMENTS|\n[A-Z][A-Z\s]*:|\n\*\*[A-Z]|$)",
            r"\*\*OPTIMIZED\s+\w+\*\*[:\s]*\n?(.*?)(?=\n\n|\n\*\*[A-Z]|\n[A-Z][A-Z\s]*:|$)",
            r"IMPROVED VERSION[:\s]*\n?(.*?)(?=\n\n|\nKEY IMPROVEMENTS|\n[A-Z][A-Z\s]*:|\n\*\*[A-Z]|$)",
            r"REWRITTEN[:\s]*\n?(.*?)(?=\n\n|\nKEY IMPROVEMENTS|\n[A-Z][A-Z\s]*:|\n\*\*[A-Z]|$)",
            r"\*\*IMPROVED VERSION\*\*[:\s]*\n?(.*?)(?=\n\n|\n\*\*[A-Z]|\n[A-Z][A-Z\s]*:|$)",
            r"ENHANCED[:\s]*\n?(.*?)(?=\n\n|\nKEY IMPROVEMENTS|\n[A-Z][A-Z\s]*:|\n\*\*[A-Z]|$)",
            r"FINAL VERSION[:\s]*\n?(.*?)(?=\n\n|\nKEY IMPROVEMENTS|\n[A-Z][A-Z\s]*:|\n\*\*[A-Z]|$)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                content = match.group(1).strip()
                # Clean up the content
                content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Remove bold formatting
                content = re.sub(r'\*(.*?)\*', r'\1', content)      # Remove italic formatting
                content = content.strip(' \n"\'')
                
                if len(content) > 20:  # Ensure we have substantial content
                    logger.info(f"Found optimized content: {content[:100]}...")
                    return content
        
        # If no specific optimized content found, try to extract any substantial paragraph
        logger.warning("No specific optimized content pattern found, trying general extraction...")
        
        # Look for substantial paragraphs that might be the optimized content
        paragraphs = text.split('\n\n')
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            # Skip if it's too short, looks like a header, or contains common section indicators
            if (len(paragraph) > 50 and 
                not paragraph.isupper() and 
                not paragraph.startswith('**') and 
                'IMPROVEMENTS' not in paragraph.upper() and
                'KEYWORDS' not in paragraph.upper()):
                
                # Clean up formatting
                paragraph = re.sub(r'\*\*(.*?)\*\*', r'\1', paragraph)
                paragraph = re.sub(r'\*(.*?)\*', r'\1', paragraph)
                paragraph = paragraph.strip(' \n"\'')
                
                logger.info(f"Using general paragraph as optimized content: {paragraph[:100]}...")
                return paragraph
        
        return "Enhanced content with improved keywords and professional language - see detailed explanation below"
    
    def _extract_alternatives(self, text: str) -> List[str]:
        """Extract alternative versions from text"""
        import re
        
        # Look for alternative versions
        patterns = [
            r"ALTERNATIVE[S]?[:\s]*\n?(.*?)(?=\n\n|\n[A-Z][A-Z\s]*:|\n\*\*[A-Z]|$)",
            r"\*\*ALTERNATIVE[S]?\*\*[:\s]*\n?(.*?)(?=\n\n|\n\*\*[A-Z]|\n[A-Z][A-Z\s]*:|$)",
            r"VERSION[S]?[:\s]*\n?(.*?)(?=\n\n|\n[A-Z][A-Z\s]*:|\n\*\*[A-Z]|$)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                section_text = match.group(1)
                # Split by version indicators
                alternatives = re.split(r'(?:Version|Alternative)\s*\d+[:\.]?', section_text)
                cleaned_alternatives = []
                for alt in alternatives:
                    alt = alt.strip()
                    if len(alt) > 20:  # Only substantial alternatives
                        # Clean up formatting
                        alt = re.sub(r'\*\*(.*?)\*\*', r'\1', alt)
                        alt = re.sub(r'\*(.*?)\*', r'\1', alt)
                        cleaned_alternatives.append(alt)
                
                if cleaned_alternatives:
                    return cleaned_alternatives
        
        return ["Alternative versions available in detailed explanation"]
    
    def _calculate_completeness(self, profile_data: Dict[str, Any]) -> int:
        """Calculate profile completeness percentage"""
        score = 0
        
        # Basic info (30 points)
        if profile_data.get('name'): score += 5
        if profile_data.get('headline'): score += 10
        if profile_data.get('summary'): score += 15
        
        # Experience (25 points)
        if profile_data.get('experience'): score += 25
        
        # Education (15 points)
        if profile_data.get('education'): score += 15
        
        # Skills (15 points)
        skills_count = len(profile_data.get('skills', []))
        if skills_count >= 10: score += 15
        elif skills_count >= 5: score += 10
        elif skills_count > 0: score += 5
        
        # Additional sections (15 points)
        if profile_data.get('certifications'): score += 5
        if profile_data.get('languages'): score += 5
        if profile_data.get('volunteer'): score += 5
        
        return min(score, 100)
    
    def _get_fallback_analysis(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback analysis when AI fails"""
        return {
            "overall_score": 70,
            "section_scores": {"headline": 75, "summary": 70, "experience": 80, "education": 75, "skills": 65},
            "strengths": ["Professional experience", "Educational background", "Skill diversity"],
            "weaknesses": ["Profile could be more detailed", "Consider adding more keywords"],
            "recommendations": ["Enhance summary section", "Add more specific achievements", "Include relevant certifications"],
            "keywords": ["Industry-specific terms", "Technical skills", "Leadership keywords"],
            "detailed_feedback": "Profile analysis completed with basic assessment. For detailed insights, please try again.",
            "profile_completeness": self._calculate_completeness(profile_data)
        }
    
    def _get_fallback_job_fit(self) -> Dict[str, Any]:
        """Fallback job fit analysis"""
        return {
            "fit_score": 65,
            "skill_match": 70,
            "experience_match": 75,
            "education_match": 80,
            "missing_skills": ["Specific technical skills may be needed"],
            "advantages": ["Relevant experience", "Strong educational background"],
            "recommendations": ["Highlight relevant achievements", "Customize profile for this role"],
            "application_tips": ["Tailor resume to job requirements", "Emphasize matching skills"],
            "detailed_analysis": "Job fit analysis completed with basic assessment."
        }
    
    def _get_fallback_optimization(self, section: str) -> Dict[str, Any]:
        """Fallback content optimization"""
        return {
            "section": section,
            "original_content": f"Current {section} content",
            "optimized_content": f"Optimized {section} with enhanced keywords and impact statements",
            "improvements": ["Added power words", "Included quantifiable achievements", "Improved keyword density"],
            "keywords_added": ["Industry terms", "Technical skills", "Action verbs"],
            "alternatives": ["Alternative version 1", "Alternative version 2"],
            "detailed_explanation": f"{section.title()} optimization completed with standard improvements."
        }
    
    def _get_fallback_career_guidance(self) -> Dict[str, Any]:
        """Fallback career guidance"""
        return {
            "career_stage": "Professional",
            "growth_opportunities": ["Senior roles in current field", "Leadership positions", "Specialized expertise areas"],
            "skill_priorities": ["Leadership skills", "Technical expertise", "Industry certifications"],
            "learning_resources": ["Professional courses", "Industry certifications", "Networking events"],
            "networking_strategy": ["Industry associations", "Professional meetups", "LinkedIn connections"],
            "market_trends": ["Digital transformation", "Remote work adaptation", "Skill diversification"],
            "action_plan": ["Update skills", "Expand network", "Seek mentorship opportunities"],
            "detailed_guidance": "Career guidance provided with general professional development recommendations."
        }
    
    def _get_enhanced_fallback_analysis(self, profile_data: Dict[str, Any], ai_response: str = "") -> Dict[str, Any]:
        """Enhanced fallback analysis with better content based on actual profile data"""
        
        # Analyze the actual profile data to provide better fallback content
        name = profile_data.get('name', 'User')
        headline = profile_data.get('headline', '')
        summary = profile_data.get('summary', '')
        experience = profile_data.get('experience', [])
        education = profile_data.get('education', [])
        skills = profile_data.get('skills', [])
        
        # Generate detailed contextual strengths
        strengths = []
        if experience:
            years_exp = len(experience) * 1.5  # Estimate years
            strengths.append(f"Demonstrates {years_exp:.1f}+ years of progressive career growth across {len(experience)} positions, showing consistent professional development and advancement")
        if len(skills) >= 15:
            strengths.append(f"Extensive skill portfolio with {len(skills)} competencies listed, indicating versatility and comprehensive expertise across multiple domains")
        elif len(skills) >= 10:
            strengths.append(f"Well-rounded skill set with {len(skills)} skills demonstrated, showing good technical and professional breadth")
        if education:
            school = education[0].get('school', 'reputable institution')
            degree = education[0].get('degree', 'degree')
            strengths.append(f"Strong educational foundation with {degree} from {school}, providing credibility and theoretical knowledge base")
        if headline and len(headline) > 30:
            strengths.append(f"Compelling professional headline ({len(headline)} characters) that effectively communicates value proposition and career focus")
        if summary and len(summary) > 200:
            strengths.append(f"Comprehensive professional summary ({len(summary)} characters) that provides detailed context about experience, achievements, and career objectives")
        if len(experience) >= 3:
            strengths.append("Demonstrates career stability and growth trajectory with multiple positions, indicating reliability and continuous learning")
        
        # Generate detailed contextual weaknesses
        weaknesses = []
        if not summary or len(summary) < 100:
            weaknesses.append("Professional summary is missing or too brief - LinkedIn profiles with detailed summaries receive 40% more profile views and are 5x more likely to receive connection requests")
        if len(skills) < 10:
            weaknesses.append(f"Skills section only lists {len(skills)} competencies - profiles with 10+ skills appear in 17x more searches and demonstrate broader expertise to recruiters")
        if not headline or len(headline) < 20:
            weaknesses.append("Headline is too brief or generic - compelling headlines increase profile visibility by 14x and should include role, key skills, and value proposition")
        if len(experience) < 2:
            weaknesses.append("Limited work experience documentation - detailed experience descriptions with achievements increase recruiter interest by 6x")
        if not any('achieve' in exp.get('description', '').lower() or 'result' in exp.get('description', '').lower() for exp in experience):
            weaknesses.append("Experience descriptions lack quantifiable achievements - profiles with metrics and results are 3x more likely to receive interview requests")
        
        # Generate detailed contextual recommendations
        recommendations = []
        recommendations.append("Add 3-5 quantifiable achievements per role (e.g., 'Increased sales by 25%', 'Led team of 8 people', 'Reduced costs by $50K annually') to demonstrate concrete impact and value")
        recommendations.append("Incorporate 15-20 industry-specific keywords throughout your profile to improve ATS compatibility and increase search visibility by up to 40%")
        recommendations.append("Request 3-5 LinkedIn recommendations from supervisors, colleagues, and clients to build social proof and increase profile credibility by 85%")
        if not summary or len(summary) < 100:
            recommendations.append("Write a 150-300 word professional summary highlighting your top 3 achievements, core competencies, and career objectives to increase profile engagement by 40%")
        if len(skills) < 15:
            recommendations.append("Add 5-10 more relevant skills including both technical competencies and soft skills, prioritizing those most relevant to your target roles")
        recommendations.append("Update your profile monthly with latest projects, certifications, and accomplishments to maintain relevance and appear in 'recent activity' feeds")
        recommendations.append("Add a professional headshot if missing - profiles with photos receive 21x more profile views and 36x more messages")
        recommendations.append("Include 2-3 relevant certifications or courses to demonstrate continuous learning and stay competitive in your field")
        
        # Generate relevant keywords based on profile
        keywords = []
        if 'software' in headline.lower() or any('software' in exp.get('title', '').lower() for exp in experience):
            keywords.extend(["Software Development", "Programming", "Technical Leadership"])
        if 'manager' in headline.lower() or any('manager' in exp.get('title', '').lower() for exp in experience):
            keywords.extend(["Team Leadership", "Project Management", "Strategic Planning"])
        if 'engineer' in headline.lower() or any('engineer' in exp.get('title', '').lower() for exp in experience):
            keywords.extend(["Engineering", "Problem Solving", "Technical Expertise"])
        
        # Add generic keywords if none found
        if not keywords:
            keywords = ["Professional Development", "Team Collaboration", "Results-Driven", "Industry Expertise", "Communication Skills"]
        
        return {
            "overall_score": 75,
            "section_scores": {
                "headline": 80 if headline and len(headline) > 20 else 60,
                "summary": 80 if summary and len(summary) > 100 else 50,
                "experience": min(70 + len(experience) * 10, 90),
                "education": 80 if education else 60,
                "skills": min(60 + len(skills) * 2, 90)
            },
            "strengths": strengths[:5] if strengths else ["Professional profile with good foundation"],
            "weaknesses": weaknesses[:5] if weaknesses else ["Profile could benefit from more detailed content"],
            "recommendations": recommendations[:6],
            "keywords": keywords[:5],
            "detailed_feedback": ai_response if ai_response else f"Profile analysis completed for {name}. The profile shows good professional foundation with opportunities for enhancement in content detail and keyword optimization.",
            "profile_completeness": self._calculate_completeness(profile_data)
        }

# Global agent instance
linkedin_agent = LinkedInOptimizerAgent()

# Convenience functions
def analyze_profile(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze LinkedIn profile"""
    return linkedin_agent.analyze_profile(profile_data)

def analyze_job_fit(profile_data: Dict[str, Any], job_description: str) -> Dict[str, Any]:
    """Analyze job fit"""
    return linkedin_agent.analyze_job_fit(profile_data, job_description)

def optimize_content(profile_data: Dict[str, Any], section: str, target_role: str = "") -> Dict[str, Any]:
    """Optimize profile content"""
    return linkedin_agent.optimize_content(profile_data, section, target_role)

def provide_career_guidance(profile_data: Dict[str, Any], career_goals: str = "") -> Dict[str, Any]:
    """Provide career guidance"""
    return linkedin_agent.provide_career_guidance(profile_data, career_goals)

def chat_with_agent(message: str, profile_data: Optional[Dict[str, Any]] = None, context: Optional[List[Dict]] = None) -> str:
    """Chat with the LinkedIn optimizer agent"""
    return linkedin_agent.chat_response(message, profile_data, context)
