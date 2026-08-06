import { useState } from "react";
import { Link } from "react-router-dom";
import "../styles/register.css";

function Register() { 
  const [formData, setFormData] = useState({
    name: "",
    district: "",
    email: "",
    password: "",
    role: "Citizen"
  });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");
    setIsSubmitting(true);

    try {
      const response = await fetch("/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          password: formData.password,
          district: formData.district,
          role: formData.role
        })
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.message || "Registration failed.");
      }

      setMessage(data.message || "Registration successful.");
      window.location.href = "/login";
    } catch (err) {
      setError(err.message || "Unable to register right now.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="register-page">
      <div className="register-card">
        <Link to="/login" className="close-btn">
          &times;
        </Link>

        <h1>Create Account</h1>

        <form onSubmit={handleRegister}>
          <input
            type="text"
            name="name"
            placeholder="Full Name"
            value={formData.name}
            onChange={handleChange}
            required
          />

          <select
            name="district"
            value={formData.district}
            onChange={handleChange}
            required
          >
            <option value="">Select District</option>
            <option value="Almora">Almora</option>
            <option value="Bageshwar">Bageshwar</option>
            <option value="Chamoli">Chamoli</option>
            <option value="Champawat">Champawat</option>
            <option value="Dehradun">Dehradun</option>
            <option value="Haridwar">Haridwar</option>
            <option value="Nainital">Nainital</option>
            <option value="Pauri Garhwal">Pauri Garhwal</option>
            <option value="Pithoragarh">Pithoragarh</option>
            <option value="Rudraprayag">Rudraprayag</option>
            <option value="Tehri Garhwal">Tehri Garhwal</option>
            <option value="Udham Singh Nagar">Udham Singh Nagar</option>
            <option value="Uttarkashi">Uttarkashi</option>
          </select>

          <input
            type="email"
            name="email"
            placeholder="Email Address"
            value={formData.email}
            onChange={handleChange}
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />

          <select
            className="register-select"
            name="role"
            value={formData.role}
            onChange={handleChange}
            required
          >
            <option value="Citizen">Driver</option>
            <option value="Official">Official</option>
          </select>

          {message && <p className="success-message">{message}</p>}
          {error && <p className="error-message">{error}</p>}

          <button className="register-btn" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Registering..." : "Register"}
          </button>
        </form>

        <p className="login-text">Already have an account?</p>

        <Link to="/login" className="login-link">
          Login
        </Link>
      </div>
    </div>
  );
}

  export default Register;