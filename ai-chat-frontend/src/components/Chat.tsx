import React, { useState, useRef, useEffect } from "react";
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  CircularProgress,
  useTheme,
} from "@mui/material";

interface Message {
  sender: "user" | "bot";
  text: string;
}

const CHAT_BOX_WIDTH = 400;
const CHAT_BOX_HEIGHT = "95vh";

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const theme = useTheme();

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { sender: "user" as const, text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    try {
      // Replace this URL with your backend endpoint
      const response = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMessage.text }),
      });
      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: data.answer || "No response from AI." },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Error contacting AI backend." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <Box
      sx={{
        minHeight: "100vh",
        minWidth: "100vw",
        bgcolor: theme.palette.background.default,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        position: "fixed",
        top: 0,
        left: 0,
        zIndex: 10,
      }}
    >
      <Paper
        elevation={6}
        sx={{
          width: CHAT_BOX_WIDTH,
          height: CHAT_BOX_HEIGHT,
          display: "flex",
          flexDirection: "column",
          borderRadius: 4,
          boxShadow: 6,
          overflow: "hidden",
          bgcolor: theme.palette.background.paper,
        }}
      >
        <Box
          sx={{
            flex: 1,
            overflowY: "auto",
            p: 2,
            bgcolor: theme.palette.background.paper,
            minHeight: 0,
          }}
        >
          {messages.map((msg, idx) => (
            <Box
              key={idx}
              sx={{
                display: "flex",
                justifyContent:
                  msg.sender === "user" ? "flex-end" : "flex-start",
                mb: 1.5,
              }}
            >
              <Paper
                elevation={2}
                sx={{
                  p: 1.5,
                  maxWidth: "75%",
                  bgcolor:
                    msg.sender === "user"
                      ? theme.palette.primary.main
                      : theme.palette.grey[800],
                  color:
                    msg.sender === "user"
                      ? theme.palette.background.paper
                      : theme.palette.text.primary,
                  borderRadius: 3,
                  borderTopRightRadius: msg.sender === "user" ? 0 : 12,
                  borderTopLeftRadius: msg.sender === "user" ? 12 : 0,
                }}
              >
                <Typography variant="body1" sx={{ wordBreak: "break-word" }}>
                  {msg.text}
                </Typography>
              </Paper>
            </Box>
          ))}
          {loading && (
            <Box
              sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1.5 }}
            >
              <CircularProgress size={18} color="primary" />
              <Typography variant="body2" color="text.secondary">
                Thinking...
              </Typography>
            </Box>
          )}
          <div ref={messagesEndRef} />
        </Box>
        <Paper
          elevation={3}
          sx={{
            p: 2,
            borderTop: `1px solid ${theme.palette.divider}`,
            display: "flex",
            alignItems: "center",
            position: "sticky",
            bottom: 0,
            bgcolor: theme.palette.background.paper,
            borderRadius: 0,
          }}
        >
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            disabled={loading}
            sx={{
              mr: 2,
              "& .MuiInputBase-root": {
                color: theme.palette.text.primary,
                bgcolor: theme.palette.grey[900],
              },
              "& .MuiOutlinedInput-notchedOutline": {
                borderColor: theme.palette.divider,
              },
              input: {
                color: theme.palette.text.primary,
              },
            }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            sx={{ fontWeight: 600 }}
          >
            Send
          </Button>
        </Paper>
      </Paper>
    </Box>
  );
};

export default Chat;
