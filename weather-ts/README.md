# Weather TypeScript Backend

This directory contains the TypeScript backend for weather data services. It provides an API to fetch current weather information for any city using the Open-Meteo API and is designed for integration with AI agents or other services.

## Features

- Fetch current weather for any city
- JSON schema validation with Zod
- Ready for integration with LLMs or chatbots

## Setup

1. Install dependencies:
   ```sh
   pnpm install
   # or
   npm install
   ```

## Usage

Run the main server:

```sh
pnpm start
# or
node src/main.ts
```

The server exposes a tool to get the weather for a given city. You can integrate this with AI agents or call it directly.

## Project Structure

```
weather-ts/
  ├── src/
  │   └── main.ts
  ├── package.json
  ├── pnpm-lock.yaml
  └── README.md
```

## License

MIT License
