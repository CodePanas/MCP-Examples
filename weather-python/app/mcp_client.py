import asyncio
import json
import os
import sys

from app.config import Config
from app.exceptions import MCPConnectionError, MCPToolError

mcp_process = None
mcp_writer = None
mcp_reader = None
mcp_initialized = False

async def start_mcp_subprocess():
    global mcp_process, mcp_writer, mcp_reader
    if mcp_process is not None:
        return

    try:
        mcp_process = await asyncio.create_subprocess_exec(
            sys.executable, os.path.join(os.path.dirname(__file__), "..", "main.py"), "--mcp-stdio",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        mcp_writer = mcp_process.stdin
        mcp_reader = mcp_process.stdout
    except Exception as e:
        raise MCPConnectionError(f"Failed to start MCP subprocess: {str(e)}")

async def stop_mcp_subprocess():
    global mcp_process
    if mcp_process:
        mcp_process.terminate()
        await mcp_process.wait()
        mcp_process = None

async def initialize_mcp():
    global mcp_initialized
    if mcp_initialized:
        return

    await start_mcp_subprocess()

    # MCP handshake: initialize
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": Config.MCP_PROTOCOL_VERSION,
            "capabilities": {
                "tools": {}
            },
            "clientInfo": {
                "name": Config.MCP_CLIENT_NAME,
                "version": Config.MCP_CLIENT_VERSION
            }
        }
    }

    try:
        mcp_writer.write((json.dumps(init_request) + "\n").encode())
        await mcp_writer.drain()

        # Read initialize response (required by MCP protocol)
        await mcp_reader.readline()

        # Send initialized notification
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }

        mcp_writer.write((json.dumps(initialized_notification) + "\n").encode())
        await mcp_writer.drain()

        mcp_initialized = True
    except Exception as e:
        raise MCPConnectionError(f"Failed to initialize MCP: {str(e)}")

async def call_mcp_tool(tool_name: str, params: dict) -> str:
    await initialize_mcp()

    # MCP protocol: tools/call method with proper format
    request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": params
        }
    }

    try:
        mcp_writer.write((json.dumps(request) + "\n").encode())
        await mcp_writer.drain()

        response_line = await mcp_reader.readline()

        response = json.loads(response_line.decode())

        if "result" in response:
            if "content" in response["result"] and len(response["result"]["content"]) > 0:
                return response["result"]["content"][0]["text"]
            else:
                return str(response["result"])
        elif "error" in response:
            raise MCPToolError(f"MCP tool error: {response['error']['message']}")
        else:
            raise MCPToolError("No result from MCP")

    except json.JSONDecodeError as e:
        raise MCPToolError(f"Error parsing MCP response: {str(e)}")
    except Exception as e:
        raise MCPToolError(f"Unexpected MCP error: {str(e)}")