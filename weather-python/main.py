import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--mcp-stdio":
        from mcp_tools.weather import mcp
        mcp.run(transport='stdio')
    else:
        import uvicorn
        uvicorn.run("app.api:app", host="0.0.0.0", port=8005, reload=True)