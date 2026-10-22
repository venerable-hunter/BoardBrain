"use client";

import { useState, useRef, useEffect } from "react";
import { chatAI, type AIChatResponse } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface AIChatSidebarProps {
  boardId: number | null;
  userId: number | null;
  onBoardUpdate?: (update: any) => void;
}

export const AIChatSidebar = ({ boardId, userId, onBoardUpdate }: AIChatSidebarProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !boardId || !userId) return;

    const userMessage: Message = { role: "user", content: input };
    setInput("");
    setIsLoading(true);

    try {
      const response: AIChatResponse = await chatAI({
        message: input,
        board_id: boardId,
        user_id: userId,
        conversation_history: [...messages, userMessage],
      });

      const assistantMessage: Message = { role: "assistant", content: response.response };
      setMessages((prev) => [...prev, userMessage, assistantMessage]);

      // Apply board update if provided
      if (response.board_update && onBoardUpdate) {
        onBoardUpdate(response.board_update);
      }
    } catch (error) {
      console.error("Failed to chat with AI:", error);
      const errorMessage: Message = {
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again.",
      };
      setMessages((prev) => [...prev, userMessage, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-[var(--secondary-purple)] text-white shadow-[var(--shadow)] hover:opacity-90 transition-all flex items-center justify-center z-50"
        title="Open AI Chat"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
        </svg>
      </button>
    );
  }

  return (
    <div className="fixed right-0 top-0 h-full w-96 bg-white border-l border-[var(--stroke)] shadow-[var(--shadow)] z-50 flex flex-col">
      <div className="flex items-center justify-between p-4 border-b border-[var(--stroke)]">
        <h2 className="font-display text-lg font-semibold text-[var(--navy-dark)]">
          AI Assistant
        </h2>
        <button
          onClick={() => setIsOpen(false)}
          className="p-2 rounded-lg hover:bg-[var(--surface)] transition-all"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-[var(--gray-text)] text-sm mt-8">
            <p>Ask me anything about your Kanban board!</p>
            <p className="mt-2 text-xs">I can help you organize tasks or suggest improvements.</p>
          </div>
        )}
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                message.role === "user"
                  ? "bg-[var(--secondary-purple)] text-white"
                  : "bg-[var(--surface)] text-[var(--navy-dark)]"
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-[var(--surface)] rounded-2xl px-4 py-3">
              <p className="text-sm text-[var(--gray-text)]">Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t border-[var(--stroke)]">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            className="flex-1 px-4 py-3 rounded-xl border border-[var(--stroke)] bg-[var(--surface)] text-[var(--navy-dark)] placeholder:text-[var(--gray-text)] focus:outline-none focus:ring-2 focus:ring-[var(--primary-blue)] focus:border-transparent transition-all resize-none"
            rows={1}
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="px-4 py-3 rounded-xl bg-[var(--secondary-purple)] text-white font-semibold hover:bg-opacity-90 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="22" y1="2" x2="11" y2="13" />
              <polygon points="22 2 15 22 11 13" />
              <path d="M11 13L9 11" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};
