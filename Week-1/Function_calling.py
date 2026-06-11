import os
import json
from groq import Groq

# Set API key from environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "generate_creatomate_json",
            "description": "Generate Creatomate video JSON",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "width": {"type": "number"},
                    "height": {"type": "number"},
                    "scenes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "duration": {"type": "number"},
                                "image_url": {"type": "string"}
                            }
                        }
                    }
                },
                "required": ["title", "scenes"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": "Create a 10 second promo video for a coffee brand"
        }
    ],
    tools=tools,
    tool_choice="auto"
)

tool_call = response.choices[0].message.tool_calls[0]
arguments = tool_call.function.arguments

data = json.loads(arguments)

print(data)