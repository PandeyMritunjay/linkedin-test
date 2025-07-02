"""
LinkedIn Profile Scraper using Apify Client SDK
Uses the working approach from test_apify_scrape.py with ApifyClient task execution.
"""

import logging
import time
from typing import Dict, Any, Optional

from apify_client import ApifyClient

from config import AppConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DirectLinkedInScraper:
    """Scrapes LinkedIn profiles using ApifyClient with saved task execution."""

    def __init__(self) -> None:
        self.api_key: str = AppConfig.APIFY_API_KEY
        self.task_id: str = AppConfig.APIFY_LINKEDIN_ACTOR
        self.client = ApifyClient(self.api_key)

    # ------------- Public API -------------

    def scrape_profile(self, profile_url: str) -> Dict[str, Any]:
        """Return standardized profile data or mock data on failure."""
        logger.info(f"Scraping LinkedIn profile: {profile_url}")

        if not self._is_valid_linkedin_url(profile_url):
            logger.error("Invalid LinkedIn profile URL supplied")
            return self._get_mock_profile_data(profile_url)

        try:
            data = self._scrape_via_apify(profile_url)
            if data:
                logger.info("Profile scraped successfully")
                return self._standardize_profile_data(data)
            logger.warning("Empty response – falling back to mock data")
        except Exception as exc:
            logger.error(f"Apify scraping error: {exc}")

        return self._get_mock_profile_data(profile_url)

    # ------------- Internal helpers -------------

    def _scrape_via_apify(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Run saved task and return the first dataset item, if any.
        Uses the working approach from test_apify_scrape.py
        """
        # Input format that works with the saved task
        task_input = {
            "profileUrls": [url]
        }

        logger.info("Starting saved task run...")
        run = self.client.task(self.task_id).call(task_input=task_input)
        
        logger.info("Task run started successfully.")

        # Retrieve dataset results
        if run and "defaultDatasetId" in run:
            dataset = self.client.dataset(run["defaultDatasetId"])
            items = dataset.list_items().items

            if items:
                logger.info("Scraped profile data successfully")
                return items[0]  # Return first item
            else:
                logger.warning("No items returned in the dataset.")
                return None
        else:
            logger.error("No dataset ID found in run result. Task may have failed.")
            return None

    @staticmethod
    def _is_valid_linkedin_url(url: str) -> bool:
        """Basic validation for LinkedIn profile URLs."""
        url = url.lower()
        return url.startswith("https://www.linkedin.com/in/") or url.startswith(
            "linkedin.com/in/"
        )

    @staticmethod
    def _standardize_profile_data(raw: Dict[str, Any]) -> Dict[str, Any]:
        """Map Apify fields to internal schema expected by agents."""
        try:
            # Map the actual fields returned by the scraper
            return {
                "name": raw.get("fullName") or raw.get("firstName", "") + " " + raw.get("lastName", ""),
                "headline": raw.get("headline") or "",
                "location": raw.get("addressWithCountry") or raw.get("addressWithoutCountry") or "",
                "summary": raw.get("about") or "",
                "experience": raw.get("experiences") or [],
                "education": raw.get("educations") or [],
                "skills": [skill.get("title", "") for skill in raw.get("skills", []) if skill.get("title")],
                "connections": raw.get("connections", 0),
                "profile_url": raw.get("linkedinUrl") or "",
                "profile_image": raw.get("profilePic") or raw.get("profilePicHighQuality") or "",
                "industry": raw.get("companyIndustry") or "",
                "company": raw.get("companyName") or "",
                "school": raw.get("educations", [{}])[0].get("title", "") if raw.get("educations") else "",
                "languages": raw.get("languages") or [],
                "certifications": raw.get("licenseAndCertificates") or [],
                "volunteer": raw.get("volunteerAndAwards") or [],
                "projects": raw.get("projects") or [],
                "raw_data": raw,
            }
        except Exception as exc:
            logger.error(f"Standardization error: {exc}")
            return DirectLinkedInScraper._get_mock_profile_data()

    @staticmethod
    def _get_mock_profile_data(profile_url: str = "") -> Dict[str, Any]:
        """Return comprehensive mock profile data for demonstration."""
        return {
            "name": "Sarah Johnson",
            "headline": "Senior Software Engineer | Full-Stack Developer | Tech Lead",
            "location": "San Francisco, California, United States",
            "summary": (
                "Experienced Senior Software Engineer with 7+ years of expertise "
                "in full-stack development, team leadership, and scalable system architecture. "
                "Passionate about building innovative solutions that drive business growth and "
                "enhance user experience. Proven track record of leading cross-functional teams "
                "and delivering high-quality software products in fast-paced environments.\n\n"
                "Key Achievements:\n"
                "• Led development of microservices architecture serving 2M+ users\n"
                "• Reduced system latency by 40% through performance optimization\n"
                "• Mentored 15+ junior developers and established coding best practices\n"
                "• Architected CI/CD pipelines improving deployment efficiency by 60%"
            ),
            "experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "TechCorp Inc.",
                    "duration": "2021 - Present",
                    "location": "San Francisco, CA",
                    "description": "Lead full-stack development of enterprise SaaS platform. Manage team of 5 engineers, architect scalable solutions, and drive technical decision-making. Technologies: React, Node.js, Python, AWS, Docker, Kubernetes."
                },
                {
                    "title": "Software Engineer",
                    "company": "StartupXYZ",
                    "duration": "2019 - 2021",
                    "location": "San Francisco, CA", 
                    "description": "Developed core platform features and APIs. Built real-time data processing pipelines handling 100k+ events/minute. Implemented automated testing and deployment processes."
                },
                {
                    "title": "Junior Software Developer",
                    "company": "Digital Solutions Ltd",
                    "duration": "2017 - 2019",
                    "location": "Seattle, WA",
                    "description": "Contributed to web application development using React and Django. Collaborated with design team to implement responsive user interfaces and optimize user experience."
                }
            ],
            "education": [
                {
                    "school": "University of California, Berkeley",
                    "degree": "Bachelor of Science in Computer Science",
                    "duration": "2013 - 2017",
                    "description": "Relevant Coursework: Data Structures, Algorithms, Software Engineering, Database Systems, Computer Networks"
                }
            ],
            "skills": [
                "JavaScript", "Python", "React", "Node.js", "AWS", "Docker", 
                "Kubernetes", "MongoDB", "PostgreSQL", "Redis", "GraphQL", 
                "REST APIs", "Microservices", "CI/CD", "Git", "Agile/Scrum",
                "Team Leadership", "System Architecture", "Performance Optimization"
            ],
            "connections": 1247,
            "profile_url": profile_url or "https://www.linkedin.com/in/sarah-johnson-dev",
            "profile_image": "https://via.placeholder.com/200x200",
            "industry": "Computer Software",
            "company": "TechCorp Inc.",
            "school": "UC Berkeley",
            "languages": [
                {"name": "English", "proficiency": "Native"},
                {"name": "Spanish", "proficiency": "Professional"}
            ],
            "certifications": [
                {
                    "name": "AWS Certified Solutions Architect",
                    "issuer": "Amazon Web Services",
                    "date": "2022"
                },
                {
                    "name": "Certified Kubernetes Administrator",
                    "issuer": "Cloud Native Computing Foundation",
                    "date": "2021"
                }
            ],
            "volunteer": [
                {
                    "organization": "Girls Who Code",
                    "role": "Volunteer Instructor",
                    "duration": "2020 - Present",
                    "description": "Teaching coding fundamentals to underrepresented youth in tech"
                }
            ],
            "raw_data": {
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "source": "mock_data",
                "profile_completeness": 95
            }
        }


# ------------- Convenience wrapper -------------

_scraper_instance = DirectLinkedInScraper()


def scrape_linkedin_profile(profile_url: str) -> Dict[str, Any]:
    """Module-level helper used by Streamlit app and agents."""
    return _scraper_instance.scrape_profile(profile_url)
