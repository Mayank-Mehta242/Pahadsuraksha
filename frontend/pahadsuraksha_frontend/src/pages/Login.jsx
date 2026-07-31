import "../styles/login.css";
import { Link } from "react-router-dom";

function Login() {
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

        <input
          type="email"
          placeholder="Enter your email"
        />

        <input
          type="password"
          placeholder="Enter your password"
        />

        <Link to="#" className="forgot-password">
          Forgot Password?
        </Link>

        <button className="login-button">
          Login
        </button>

        <p className="register-text">
          Don't have an account?
        </p>

        <Link to="/register" className="register-btn">
          Register
        </Link>

      </div>
    </div>
  );
}

export default Login;