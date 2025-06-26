import json
from openai import OpenAI
from app.config import Config
from app.exceptions import OpenAIError

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def get_tools_schema(self):
        """Get the tools schema for OpenAI function calling"""
        return [
            {
                "type": "function",
                "function": {
                    "name": Config.WEATHER_TOOL_NAME,
                    "description": Config.WEATHER_TOOL_DESCRIPTION,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {"type": "string", "description": "City name"}
                        },
                        "required": ["city"]
                    }
                }
            }
        ]

    async def process_question(self, question: str, tool_result: str = None, tool_calls=None):
        """Process a question with optional tool results"""
        messages = [{"role": "user", "content": question}]

        if tool_result and tool_calls:
            messages.extend([
                {"role": "assistant", "content": None, "tool_calls": tool_calls},
                {"role": "tool", "tool_call_id": tool_calls[0].id, "content": tool_result}
            ])

        try:
            completion = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages,
                tools=self.get_tools_schema() if not tool_result else None,
                tool_choice="auto" if not tool_result else None
            )
            return completion.choices[0].message
        except Exception as e:
            raise OpenAIError(f"OpenAI API error: {str(e)}")