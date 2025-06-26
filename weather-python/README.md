# AI Chat with MCP Weather Integration

A FastAPI backend that integrates OpenAI GPT-4 with Model Context Protocol (MCP) tools for weather information.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  React Frontend │    │  FastAPI Backend│    │   MCP Weather   │
│                 │    │                 │    │     Tool        │
│  - Chat UI      │◄──►│  - OpenAI API   │◄──►│  - Weather API  │
│  - Material UI  │    │  - MCP Client   │    │  - JSON-RPC     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Features

- 🤖 **AI-Powered Chat**: OpenAI GPT-4 with function calling
- 🌤️ **Weather Integration**: Real-time weather data via MCP
- 🔧 **MCP Protocol**: Standard Model Context Protocol implementation
- 🚀 **FastAPI Backend**: High-performance async API
- 🎨 **React Frontend**: Modern chat interface with Material UI

## Project Structure

```
weather-python/
├── app/
│   ├── api.py              # FastAPI endpoints
│   ├── config.py           # Configuration management
│   ├── exceptions.py       # Custom exceptions
│   ├── mcp_client.py       # MCP protocol client
│   └── services/
│       └── openai_service.py  # OpenAI integration service
├── mcp_tools/
│   └── weather.py          # MCP weather tool definition
├── main.py                 # MCP server entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Backend

```bash
uvicorn app.api:app --host 0.0.0.0 --port 8005 --reload
```

### 4. Run the Frontend

```bash
cd ../ai-chat-frontend
npm start
```

## API Endpoints

- `POST /api/ask` - Process questions with AI and MCP tools
- `GET /health` - Health check endpoint

## MCP Integration

The backend implements the Model Context Protocol (MCP) over stdio:

1. **Handshake**: Initialize MCP connection
2. **Tool Discovery**: Register available tools
3. **Tool Execution**: Call weather tool when needed
4. **Response Processing**: Handle MCP responses

## Development

### Adding New MCP Tools

1. Create tool definition in `mcp_tools/`
2. Update `config.py` with tool configuration
3. Add tool schema to `openai_service.py`
4. Update API logic in `api.py`

### Error Handling

The application uses custom exceptions for better error handling:

- `MCPError` - Base MCP exceptions
- `OpenAIError` - OpenAI API errors
- `WeatherAPIError` - Weather service errors

## Configuration

All configuration is centralized in `app/config.py`:

- OpenAI settings
- Server configuration
- MCP protocol settings
- CORS configuration

## Future Enhancements

- [ ] Add more MCP tools (calendar, email, etc.)
- [ ] Implement conversation history
- [ ] Add user authentication
- [ ] Support for multiple AI models
- [ ] Real-time chat with WebSockets
