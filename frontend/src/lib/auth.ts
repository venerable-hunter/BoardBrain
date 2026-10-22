import { loginUser, type LoginResponse } from "./api";

const SESSION_KEY = "pm_auth_session";
const USER_KEY = "pm_user";
const TOKEN_KEY = "pm_token";

export async function login(username: string, password: string): Promise<boolean> {
  try {
    const response: LoginResponse = await loginUser(username, password);
    sessionStorage.setItem(SESSION_KEY, "authenticated");
    sessionStorage.setItem(USER_KEY, JSON.stringify(response.user));
    sessionStorage.setItem(TOKEN_KEY, response.access_token);
    return true;
  } catch (error) {
    console.error("Login failed:", error);
    return false;
  }
}

export function logout(): void {
  sessionStorage.removeItem(SESSION_KEY);
  sessionStorage.removeItem(USER_KEY);
  sessionStorage.removeItem(TOKEN_KEY);
}

export function isAuthenticated(): boolean {
  return sessionStorage.getItem(SESSION_KEY) === "authenticated";
}

export function getUserId(): number | null {
  const userStr = sessionStorage.getItem(USER_KEY);
  if (!userStr) return null;
  const user = JSON.parse(userStr);
  return user.id;
}

export function getToken(): string | null {
  return sessionStorage.getItem(TOKEN_KEY);
}
