"use client";

import { useEffect, useState } from "react";
import { KanbanBoard } from "@/components/KanbanBoard";
import { LoginForm } from "@/components/LoginForm";
import { isAuthenticated, login } from "@/lib/auth";

export default function Home() {
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    setAuthenticated(isAuthenticated());
  }, []);

  const handleLogin = () => {
    setAuthenticated(true);
  };

  if (!authenticated) {
    return <LoginForm onLogin={handleLogin} />;
  }

  return <KanbanBoard />;
}
