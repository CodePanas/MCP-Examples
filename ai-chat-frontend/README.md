# AI Chat Frontend

This is a minimal, general-purpose chat frontend built with React and TypeScript. It allows users to interact with an AI assistant, asking any kind of question (not just about the weather). The UI is simple, clean, and easy to extend.

## Features

- Minimal and intuitive chat interface
- Message history with user/bot distinction
- Ready to connect to any AI backend (e.g., OpenAI, Claude, custom MCP server)

## Setup

1. Install dependencies:

   ```sh
   npm install
   ```

2. Start the development server:
   ```sh
   npm start
   ```
   The app will be available at [http://localhost:3000](http://localhost:3000).

## Usage

- Type your message in the input box and press Enter or click Send.
- The chat will display your message and the AI's response.
- By default, the app expects a backend endpoint at `/api/ask` that accepts POST requests with `{ question: string }` and returns `{ answer: string }`.

## Customization

- You can easily extend the UI or connect to different AI backends by modifying the fetch call in `src/components/Chat.tsx`.

## Project Structure

```
ai-chat-frontend/
  ├── src/
  │   ├── components/
  │   │   └── Chat.tsx
  │   └── App.tsx
  ├── package.json
  └── README.md
```

## License

MIT License
