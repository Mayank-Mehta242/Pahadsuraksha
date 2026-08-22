import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.js";
import LoadingSpinner from "./LoadingSpinner.jsx";

export default function ProtectedRoute({ children, requireRole }) {
  const { user, loading } = useAuth();

  if (loading) return <LoadingSpinner label="Checking your session" />;
  if (!user) return <Navigate to="/login" replace />;
  if (requireRole && user.role !== requireRole) return <Navigate to="/" replace />;

  return children;
}
