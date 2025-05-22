import datetime
import os
import asyncio
from zoneinfo import ZoneInfo
from google.adk.agents import Agent, LlmAgent, BaseAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts
from google.adk.tools import google_search
from google.adk.tools import agent_tool
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")
import logging
logging.basicConfig(level=logging.ERROR)

from multi_tool_agent.weather import get_extended_weather_forecast
from multi_tool_agent.weather import get_lat_lon
import multi_tool_agent.config_weather_agent as config_weather_agent
import multi_tool_agent.config_search_agent as config_search_agent
import multi_tool_agent.config_root_agent as config_root_agent

MODEL_GEMINI_FLASH = "gemini-2.5-flash-preview-04-17"
MODEL_GPT = "openai/gpt-4o"

OpenAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-default-api-key")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "your-default-api-key")


# Configure the weather Agent
weather_agent = LlmAgent(
    name="weather_agent",
    # model=MODEL_GEMINI_FLASH, # Can be a string for Gemini or a LiteLlm object
    model=LiteLlm(model=MODEL_GPT), # Using GPT for the Weather agent
    description=config_weather_agent.DESCRIPTION,
    instruction=config_weather_agent.INSTRUCTIONS,
    tools=[get_extended_weather_forecast, get_lat_lon], # Pass the function directly
)

google_search_agent = LlmAgent(
    name="google_search_agent",
    model=MODEL_GEMINI_FLASH, # Can be a string for Gemini or a LiteLlm object
    #model=LiteLlm(model=MODEL_GPT),
    description=config_search_agent.DESCRIPTION,
    instruction=config_search_agent.INSTRUCTIONS,
    tools=[google_search]
)


root_agent = LlmAgent(
    name="root_agent",
    model=MODEL_GEMINI_FLASH, # Can be a string for Gemini or a LiteLlm object
    description=config_root_agent.DESCRIPTION,
    instruction=config_root_agent.INSTRUCTIONS,
    tools=[agent_tool.AgentTool(agent=google_search_agent)],
    sub_agents=[weather_agent],
)

