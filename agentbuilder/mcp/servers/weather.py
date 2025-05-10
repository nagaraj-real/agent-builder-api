from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("Weather")

class WeatherParams(BaseModel):
    city: str = Field(..., description="The name of the city to get the weather for.")
    units: str = Field("metric", description="Unit system: 'metric' (Celsius) or 'imperial' (Fahrenheit)")

@mcp.tool()
def get_weather(params: WeatherParams) -> str:
    """Get weather for city."""
    return f"It's 30 degree {params.units} in {params.city}"

if __name__ == "__main__":
    mcp.run(transport="stdio")