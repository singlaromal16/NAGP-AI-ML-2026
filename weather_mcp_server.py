import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Weather Server",
    instructions=(
        "This MCP server provides weather-related tools. "
        "Use find_city to resolve a city name to coordinates and get_weather "
        "to fetch current weather data for those coordinates."
    ),
)

@mcp.tool(description="Find the latitude and longitude of a city by name.")
def find_city(city: str) -> dict:
    """Find the latitude and longitude of a city."""

    try:
        response = httpx.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        response.raise_for_status()
        results = response.json().get("results", [])
        if not results:
            return {
                "success": False,
                "error": f"City not found: {city}"
            }

        data = results[0]
        return {
            "success": True,
            "name": data["name"],
            "country": data.get("country"),
            "latitude": data["latitude"],
            "longitude": data["longitude"],
        }
    except httpx.HTTPError as e:
        return {
            "success": False,
            "error": f"City search service failed: {str(e)}"
        }


@mcp.tool(description="Get the current weather for a latitude and longitude pair.")
def get_weather(latitude: float, longitude: float, forecastDays: int) -> dict:
    """Get current weather for coordinates."""

    try:
        response = httpx.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
                "daily": (
                    "weather_code,"
                    "temperature_2m_max,"
                    "temperature_2m_min,"
                    "precipitation_probability_max"
                ),
                "forecast_days": forecastDays,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "current": data.get("current", {}),
            "forecast": data.get("daily", {}),
            "source": "Open-Meteo via Weather MCP"
        }

    except httpx.HTTPError as e:
        return {
            "success": False,
            "error": f"Weather service failed: {str(e)}"
        }

if __name__ == "__main__":
    mcp.run()