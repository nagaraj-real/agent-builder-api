
# type: ignore
import asyncio
from pathlib import Path
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool
from agentbuilder.error.error_handler import default_handle_error

async def get_weather(city:str)->str:
    """Returns current temperature for a given city name in celsius"""
     # Ideally we will be calling an API to get latest temperature here
    await asyncio.sleep(0)
    return "10 degrees celsius"

class WeatherInput(BaseModel):
   city: str = Field(description="City name")


temperature_tool = StructuredTool.from_function(
    coroutine=get_weather,
    name="temperature_tool",
    description="Provides current temperature for a given city in celsius",
    handle_tool_error=default_handle_error,
    args_schema=WeatherInput
)
temperature_tool.metadata= {"file_path": str(Path(__file__).absolute())}


@tool("temperature_sensor_tool")
def temperature_sensor_tool(temperature:float)->str:
    """Returns if weather is hot or cold based on temperature input"""

    # Ideally we would make an API call to fetch current weather
    return "hot" if float(temperature) > 30  else "cold"

class IsWeatherHotColdInput(BaseModel):
   temperature: float = Field(description="Temperature of the current city in float")

temperature_sensor_tool.description = "Returns if weather is hot or cold based on input"
temperature_sensor_tool.args_schema = IsWeatherHotColdInput
temperature_sensor_tool.metadata= {"file_path": str(Path(__file__).absolute())}


def weather_clothing(temperature:float)->str:
    """Returns clothing for the given temperature input"""
    return "Cotton Shirt" if float(temperature) > 20  else "Warm Jacket"

class WeatherClothingInput(BaseModel):
   temperature: float = Field(description="Temperature of the current city in float.")

weather_clothing_tool= StructuredTool.from_function(
    func=weather_clothing,
    name="weather_clothing_tool",
    description="Returns clothing for the given temperature input",
    args_schema=WeatherClothingInput
)

weather_clothing_tool.metadata= {"file_path": str(Path(__file__).absolute())}