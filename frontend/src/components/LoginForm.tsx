"use client";

import { useState, FormEvent } from "react";
import { login } from "@/lib/auth";

interface LoginFormProps {
  onLogin: () => void;
}

export const LoginForm = ({ onLogin }: LoginFormProps) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    const success = await login(username, password);

    if (success) {
      onLogin();
    } else {
      setError("Invalid username or password");
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        <div className="rounded-[32px] border border-[var(--stroke)] bg-white/80 p-8 shadow-[var(--shadow)] backdrop-blur">
          <div className="text-center mb-8">
            <h1 className="font-display text-3xl font-semibold text-[var(--navy-dark)] mb-2">
              Welcome Back
            </h1>
            <p className="text-sm text-[var(--gray-text)]">
              Sign in to access your Kanban board
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label
                htmlFor="username"
                className="block text-xs font-semibold uppercase tracking-[0.2em] text-[var(--gray-text)] mb-2"
              >
                Username
              </label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-[var(--stroke)] bg-[var(--surface)] text-[var(--navy-dark)] placeholder:text-[var(--gray-text)] focus:outline-none focus:ring-2 focus:ring-[var(--primary-blue)] focus:border-transparent transition-all"
                placeholder="Enter your username"
                required
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-xs font-semibold uppercase tracking-[0.2em] text-[var(--gray-text)] mb-2"
              >
                Password
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-[var(--stroke)] bg-[var(--surface)] text-[var(--navy-dark)] placeholder:text-[var(--gray-text)] focus:outline-none focus:ring-2 focus:ring-[var(--primary-blue)] focus:border-transparent transition-all"
                placeholder="Enter your password"
                required
              />
            </div>

            {error && (
              <div className="p-3 rounded-lg bg-red-50 border border-red-200">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 px-4 rounded-xl bg-[var(--secondary-purple)] text-white font-semibold hover:bg-opacity-90 transition-all focus:outline-none focus:ring-2 focus:ring-[var(--secondary-purple)] focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "Signing in..." : "Sign In"}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-xs text-[var(--gray-text)]">
              Demo credentials: user / password
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
