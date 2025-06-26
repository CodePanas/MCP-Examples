import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
const server = new McpServer({
  name: "mcp",
  version: "1.0.0",
  description: "My MCP server",
});

// Define the tools that the server offers
// Tools allow the LLM to perform tasks it cannot do by itself
// Example: searching the internet, performing calculations, etc.

server.tool(
  "get weather",
  "Get the weather for a given city",
  {
    city: z.string().describe("City name"),
  },
  async ({ city }) => {
    const response = await fetch(
      `https://geocoding-api.open-meteo.com/v1/search?name=${city}&count=1&language=en&format=json`
    );

    const data = await response.json();

    if (data.length === 0) {
      return {
        content: [
          {
            type: "text",
            text: `City ${city} not found.`,
          },
        ],
      };
    }

    const { latitude, longitude } = data.results[0];

    const weatherResponse = await fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&hourly=temperature_2m&current=temperature_2m,precipitation,is_day,rain&forecast_days=1`
    );

    const weatherData = await weatherResponse.json();

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(weatherData, null, 2),
        },
      ],
    };
  }
);

//3. Listen for client connections
const transport = new StdioServerTransport();
await server.connect(transport);
