import { createContext, useEffect, useState } from "react";
import { authService } from "../services/authService.js";

export const AuthContext = createContext(null);

const TOKEN_KEY = "pahadsuraksha_token";

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // On first load, if a token is already stored, try to restore the session.
  // TODO(BACKEND): authService.getCurrentUser() currently returns mock data
  // whenever a token exists — swap in a real GET /api/auth/me call.
  useEffect(() => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token) {
      setLoading(false);
      return;
    }
    authService
      .getCurrentUser(token)
      .then((u) => setUser(u))
      .catch(() => localStorage.removeItem(TOKEN_KEY))
      .finally(() => setLoading(false));
  }, []);

  async function login(email, password) {
    // TODO(BACKEND): POST /api/auth/login -> { token, user }
    const { token, user: loggedInUser } = await authService.login(email, password);
    localStorage.setItem(TOKEN_KEY, token);
    setUser(loggedInUser);
    return loggedInUser;
  }

  async function register(payload) {
    // TODO(BACKEND): POST /api/auth/register -> { token, user }
    const { token, user: newUser } = await authService.register(payload);
    localStorage.setItem(TOKEN_KEY, token);
    setUser(newUser);
    return newUser;
  }

  function loginAsGuest() {
    setUser({ id: "guest", name: "Guest", role: "guest", district: null });
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY);
    setUser(null);
  }

  const value = { user, loading, login, register, loginAsGuest, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
