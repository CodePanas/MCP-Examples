class MCPError(Exception):
    """Base exception for MCP-related errors"""
    pass

class MCPConnectionError(MCPError):
    """Raised when MCP connection fails"""
    pass

class MCPToolError(MCPError):
    """Raised when MCP tool execution fails"""
    pass

class OpenAIError(Exception):
    """Base exception for OpenAI-related errors"""
    pass

class WeatherAPIError(Exception):
    """Raised when weather API calls fail"""
    pass