import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import Config
from app.services.openai_service import OpenAIService
from app.mcp_client import call_mcp_tool, start_mcp_subprocess, stop_mcp_subprocess
from app.exceptions import OpenAIError, MCPToolError

app = FastAPI(title="AI Chat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
openai_service = OpenAIService()

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

@app.on_event("startup")
async def startup_event():
    await start_mcp_subprocess()

@app.on_event("shutdown")
async def shutdown_event():
    await stop_mcp_subprocess()

@app.post("/api/ask", response_model=AskResponse)
async def ask_api(req: AskRequest):
    """Process a question using AI and MCP tools when needed"""
    try:
        # First call to OpenAI to determine if tools are needed
        message = await openai_service.process_question(req.question)

        # Check if tool call is needed
        if message.tool_calls and message.tool_calls[0].function.name == Config.WEATHER_TOOL_NAME:
            # Extract arguments and call MCP tool
            args = json.loads(message.tool_calls[0].function.arguments)
            tool_result = await call_mcp_tool(Config.WEATHER_TOOL_NAME, args)

            # Second call to OpenAI with tool result
            final_message = await openai_service.process_question(
                req.question,
                tool_result,
                message.tool_calls
            )

            return AskResponse(answer=final_message.content)

        return AskResponse(answer=message.content)

    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")
    except MCPToolError as e:
        raise HTTPException(status_code=500, detail=f"MCP tool error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ai-chat-api"}