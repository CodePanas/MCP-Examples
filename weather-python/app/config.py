import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4-0613"

    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8005

    # MCP Configuration
    MCP_PROTOCOL_VERSION = "2024-11-05"
    MCP_CLIENT_NAME = "fastapi-client"
    MCP_CLIENT_VERSION = "1.0.0"

    # CORS Configuration
    CORS_ORIGINS = ["*"]  # In production, specify actual origins

    # Tool Configuration
    WEATHER_TOOL_NAME = "get_weather"
    WEATHER_TOOL_DESCRIPTION = "Get the weather for a given city"