# Weather Python Backend

This directory contains the Python backend for weather data services. It provides an API to fetch current weather information for any city using the Open-Meteo API.

## Features

- Fetch current weather for any city
- Easy integration with AI agents or chatbots
- Asynchronous HTTP requests for fast responses

## Setup

1. Create and activate a virtual environment (optional but recommended):
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the main server:

```sh
python src/main.py
```

The server exposes a tool to get the weather for a given city. You can integrate this with AI agents or call it directly.

## Project Structure

```
weather-python/
  ├── src/
  │   └── main.py
  ├── requirements.txt
  └── README.md
```

## License

MIT License
