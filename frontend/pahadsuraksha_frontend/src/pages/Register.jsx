import "../styles/register.css";
import { Link } from "react-router-dom";

function Register() {
  return (
    <div className="register-page">
      <div className="register-card">

        <Link to="/login" className="close-btn">
          &times;
        </Link>

        <h1>Create Account</h1>

        <input
          type="text"
          placeholder="Full Name"
        />

        <select>
          <option value="">Select District</option>
          <option>Almora</option>
          <option>Bageshwar</option>
          <option>Chamoli</option>
          <option>Champawat</option>
          <option>Dehradun</option>
          <option>Haridwar</option>
          <option>Nainital</option>
          <option>Pauri Garhwal</option>
          <option>Pithoragarh</option>
          <option>Rudraprayag</option>
          <option>Tehri Garhwal</option>
          <option>Udham Singh Nagar</option>
          <option>Uttarkashi</option>
        </select>

        <input
          type="email"
          placeholder="Email Address"
        />

        <input
          type="password"
          placeholder="Password"
        />
         <select className="register-select">
            <option value="citizen">Register as </option>
             <option value="citizen">Driver</option>
             <option value="disaster-official">Disaster Official/RoadManagement</option>
        </select>


        <button className="register-btn">
          Register
        </button>

        <p className="login-text">
          Already have an account?
        </p>

        <Link to="/login" className="login-link">
          Login
        </Link>

      </div>
    </div>
  );
}

export default Register;