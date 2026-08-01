import { useState } from "react";
import "../styles/login.css";
import { Link } from "react-router-dom";

function Login() {

  const [role, setRole] = useState("Citizen");

  const handleLogin = async () => {

    /*
    ===============================================

        BACKEND LOGIN API

        POST /api/login

        Send

        {
            email,
            password,
            role
        }

        Backend Response

        If Citizen
            Navigate -> /dashboard

        If Disaster Official
            Navigate -> /admin

    ===============================================
    */

    console.log("Login as:", role);
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

        {/* Login As */}

        <div className="input-group">

          <label>Login As</label>

          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="Citizen">
              Citizen
            </option>

            <option value="Disaster Official">
              Disaster Official
            </option>

          </select>

        </div>

        {/* Email */}

        <div className="input-group">

          <label>Email</label>

          <input
            type="email"
            placeholder="Enter your email"
          />

        </div>

        {/* Password */}

        <div className="input-group">

          <label>Password</label>

          <input
            type="password"
            placeholder="Enter your password"
          />

        </div>

        <Link
          to="#"
          className="forgot-password"
        >
          Forgot Password?
        </Link>

        <button
          className="login-button"
          onClick={handleLogin}
        >
          Login
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

      </div>

    </div>
  );
}

export default Login;