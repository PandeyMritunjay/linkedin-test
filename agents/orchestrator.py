from agents.profile_agent import ProfileAnalysisAgent
from agents.job_fit_agent import JobFitAgent
from agents.content_optimization_agent import ContentOptimizationAgent
from agents.career_guidance_agent import CareerGuidanceAgent
from agents.chat_agent import ChatAgent

# Instantiate agents (singletons for session/persistent memory)
profile_agent = ProfileAnalysisAgent()
job_fit_agent = JobFitAgent()
content_agent = ContentOptimizationAgent()
career_agent = CareerGuidanceAgent()
chat_agent = ChatAgent()

def route_request(user_input, task_type):
    if task_type == "profile":
        return profile_agent.run({"input": user_input})
    elif task_type == "job_fit":
        return job_fit_agent.run({"input": user_input})
    elif task_type == "content":
        return content_agent.run({"input": user_input})
    elif task_type == "guidance":
        return career_agent.run({"input": user_input})
    elif task_type == "chat":
        return chat_agent.run({"input": user_input})
    else:
        return "Unknown task type." 