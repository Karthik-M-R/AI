"""


LLM's with tools is called Agents....!!




Weather Agent (Tool-Calling Agent)
-----------------------------------
This script implements an AI agent that follows a step-based loop
with tool-calling capability. The agent reasons step-by-step using
PLAN steps, can call TOOLS to fetch real data, and produces a final OUTPUT.

Flow:
  START  — User gives an input
  PLAN   — AI breaks the problem into steps (can be multiple)
  ACTION — AI decides to call a tool (e.g., get_weather)
  OBSERVE — Tool result is fed back to the AI
  OUTPUT — AI gives the final answer
"""

import os
import json
import time
import requests
from typing import Literal, Optional
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

# Load .env from current directory
load_dotenv()

# ─── Tool Definitions ───────────────────────────────────────────────────────

def get_weather(city: str) -> str:
    """Fetch current weather for a city using wttr.in (no API key needed)."""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data["current_condition"][0]
        weather_info = {
            "city": city,
            "temperature_C": current["temp_C"],
            "temperature_F": current["temp_F"],
            "feels_like_C": current["FeelsLikeC"],
            "humidity": current["humidity"] + "%",
            "description": current["weatherDesc"][0]["value"],
            "wind_speed_kmph": current["windspeedKmph"],
            "wind_direction": current["winddir16Point"],
        }
        return json.dumps(weather_info)
    except Exception as e:
        return json.dumps({"error": str(e)})


# Map of available tools
available_tools = {
    "get_weather": get_weather,
}


# ─── Pydantic Output Schema ──────────────────────────────────────────────────

class MyOutput(BaseModel):
    """Typed schema for every JSON response the LLM produces.

    The LLM always returns exactly one step of the agent loop.
    Fields that are only relevant to specific steps are Optional.

    Example (ACTION step)::

        {
            "step": "ACTION",
            "content": "Fetching weather data for London",
            "function_name": "get_weather",
            "input": "London"
        }

    Example (OUTPUT step)::

        {
            "step": "OUTPUT",
            "content": "It is currently 15°C in London with partly cloudy skies."
        }
    """

    step: Literal["START", "PLAN", "ACTION", "OBSERVE", "OUTPUT"] = Field(
        ..., description="Current step in the agent reasoning loop."
    )
    content: str = Field(
        ..., description="Human-readable description or final answer for this step."
    )
    # Only present during an ACTION step
    function_name: Optional[str] = Field(
        default=None,
        alias="function",
        description="Tool to call — only set when step is ACTION."
    )
    input: Optional[str] = Field(
        default=None,
        description="Input passed to the tool — only set when step is ACTION."
    )

    model_config = {"populate_by_name": True}

# ─── System Prompt ───────────────────────────────────────────────────────────

System_prompt = """
You are a helpful Weather AI assistant. You work by running a start, plan, action, observe, and output loop.
For the given user query, analyse the query and break it down into sub-tasks.
- Strictly follow the given JSON output format.
- Only run one step at a time.
- The sequence of steps is:
    START   — where user gives an input
    PLAN    — reason about what to do (can be multiple times)
    ACTION  — call a tool to get real data
    OBSERVE — after the tool returns, you observe the result (system will provide this)
    OUTPUT  — give the final answer to the user

Available Tools:
- get_weather: Takes a city name as input and returns the current weather data.
  Input: { "function": "get_weather", "input": "CityName" }

Output JSON Format (MyOutput schema):
{ "step": "START" | "PLAN" | "ACTION" | "OBSERVE" | "OUTPUT", "content": "string", "function": "tool_name (only for ACTION step)", "input": "tool_input (only for ACTION step)" }

Notes:
- 'function' and 'input' are OPTIONAL — include them ONLY when step is ACTION.
- Every other step only needs 'step' and 'content'.

Example conversation for "What's the weather in London?":
{ "step": "PLAN", "content": "The user wants to know the current weather in London. I will use the get_weather tool." }
{ "step": "ACTION", "content": "Calling get_weather for London", "function": "get_weather", "input": "London" }
{ "step": "OBSERVE", "content": "Weather data received: Temperature 15°C, Humidity 72%, Partly cloudy" }
{ "step": "OUTPUT", "content": "The current weather in London is 15°C (59°F), partly cloudy with 72% humidity and winds at 12 km/h from the west." }
"""

# ─── Client Setup ────────────────────────────────────────────────────────────

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ─── Main Agent Loop ─────────────────────────────────────────────────────────

message_history = [
    {"role": "system", "content": System_prompt}
]

user_query = input("🧑‍💻 Ask about weather: ")
message_history.append({"role": "user", "content": user_query})

while True:
    # Retry logic for rate limits
    for attempt in range(5):
        try:
            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                response_format={"type": "json_object"},
                messages=message_history
            )
            break
        except Exception as e:
            error_msg = str(e)
            if "limit: 0" in error_msg:
                print(f"❌ Model not available or limit is 0. Please check API key/model: {error_msg}")
                raise e
            elif "429" in error_msg or "rate" in error_msg.lower():
                wait_time = 5 * (attempt + 1)  # 5, 10, 15, 20, 25 seconds
                print(f"⏳ Rate limited. Retrying in {wait_time}s... (Error: {e})")
                time.sleep(wait_time)
            else:
                print(f"❌ API Error: {e}")
                raise e
    else:
        print("❌ Failed after 5 retries due to rate limits.")
        print("💡 Tip: Wait a minute and try again, or check your API key quota at https://aistudio.google.com/apikey")
        break

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    # ── Validate the LLM response against the MyOutput Pydantic schema ──
    try:
        parsed: MyOutput = MyOutput.model_validate_json(raw_result)
    except Exception as parse_err:
        print("⚠️ Failed to parse/validate response:", raw_result)
        print("   Validation error:", parse_err)
        break

    if parsed.step == "START":
        print("🚀 START:", parsed.content)
        continue

    if parsed.step == "PLAN":
        print("🧠 PLAN:", parsed.content)
        continue

    if parsed.step == "ACTION":
        tool_name = parsed.function_name   # typed Optional[str]
        tool_input = parsed.input          # typed Optional[str]
        print(f"🔧 ACTION: Calling {tool_name}({tool_input})")

        if tool_name in available_tools:
            tool_result = available_tools[tool_name](tool_input)
            print(f"📡 OBSERVE: {tool_result}")

            # Feed the tool result back into the conversation
            message_history.append({
                "role": "user",
                "content": json.dumps({
                    "step": "OBSERVE",
                    "content": tool_result
                })
            })
        else:
            print(f"⚠️ Unknown tool: {tool_name}")
            break
        continue

    if parsed.step == "OBSERVE":
        print("👁️ OBSERVE:", parsed.content)
        continue

    if parsed.step == "OUTPUT":
        print("\n📦 OUTPUT:", parsed.content)
        break
