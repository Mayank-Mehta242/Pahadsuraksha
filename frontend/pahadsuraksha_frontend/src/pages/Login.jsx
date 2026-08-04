import { useState } from "react";
import "../styles/login.css";
import { Link } from "react-router-dom";

function Login() {
  const [formData, setFormData] = useState({
    email: "",
    password: ""
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password
        })
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.message || "Login failed.");
      }

      const authToken = data.token || data.access_token || "";
      const userData = data.user || {};

      if (authToken) {
        localStorage.setItem("token", authToken);
      }
      localStorage.setItem("user", JSON.stringify(userData));

      const normalizedRole = (userData.role || "").toLowerCase();
      const isAdmin = normalizedRole.includes("official") || normalizedRole.includes("admin") || normalizedRole.includes("disaster");

      window.location.href = isAdmin ? "/admin-panel" : "/dashboard";
    } catch (err) {
      setError(err.message || "Unable to sign in.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">

      <div className="login-card">

        <Link to="/" className="close-btn">
          &times;
        </Link>

        <h1>Welcome Back</h1>

        <p className="subtitle">
          Login to continue using <strong>PAHADSURAKSHA</strong>
        </p>

        <form onSubmit={handleLogin}>
        {/* Email */}

        <div className="input-group">

          <label>Email</label>

          <input
            type="email"
            name="email"
            placeholder="Enter your email"
            value={formData.email}
            onChange={handleChange}
            required
          />

        </div>

        {/* Password */}

        <div className="input-group">

          <label>Password</label>

          <input
            type="password"
            name="password"
            placeholder="Enter your password"
            value={formData.password}
            onChange={handleChange}
            required
          />

        </div>

        <Link
          to="#"
          className="forgot-password"
        >
          Forgot Password?
        </Link>

        {error && <p className="error-message">{error}</p>}

        <button
          className="login-button"
          type="submit"
          disabled={loading}
        >
          {loading ? "Signing in..." : "Login"}
        </button>

        <p className="register-text">

          Don't have an account?

        </p>

        <Link
          to="/register"
          className="register-btn"
        >
          Register
        </Link>
        </form>

      </div>

    </div>
  );
}

export default Login;