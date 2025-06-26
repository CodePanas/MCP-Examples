from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import json

# Initialize FastMCP server
mcp = FastMCP("mcp-python")

@mcp.tool(title="Get the weather for a given city", description="Get the weather for a given city")
async def get_weather(city: str) -> str:
    """Get the weather for a given city using the Open-Meteo API"""
    async with httpx.AsyncClient() as client:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_response = await client.get(geo_url)
        geo_data = geo_response.json()
        if not geo_data.get("results"):
            return f"City {city} not found."
        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
            f"&hourly=temperature_2m&current=temperature_2m,precipitation,is_day,rain&forecast_days=1"
        )
        weather_response = await client.get(weather_url)
        weather_data = weather_response.json()
        return json.dumps(weather_data)

if __name__ == "__main__":
    # Run the FastMCP server
    mcp.run(transport='stdio')