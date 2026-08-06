import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/navbar.css";
import logoimg from "../assets/ChatGPT.png";

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();

  const closeMenu = () => setMenuOpen(false);
  const storedUser = JSON.parse(localStorage.getItem("user") || "null");
  const token = localStorage.getItem("token");
  const role = (storedUser?.role || "").toLowerCase();
  const isAdmin = role.includes("official") || role.includes("admin") || role.includes("disaster");
  const isLoggedIn = !!token;

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setMenuOpen(false);
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="nav-left">
        <div className="logoimg">
          <img src={logoimg} alt="Logo" />
        </div>

        <h2 className="logo-text">
          <span className="pahad">Pahad</span>
          <span className="suraksha">Suraksha</span>
        </h2>
      </div>

      <div className="menu-container">
        <button
          className="menu-btn"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          ☰
        </button>

        {menuOpen && (
          <div className="dropdown">
            <Link to="/" className="menu-item" onClick={closeMenu}>
              Home
            </Link>

            <Link to="/dashboard" className="menu-item" onClick={closeMenu}>
              Dashboard
            </Link>

            <Link to="/weather" className="menu-item" onClick={closeMenu}>
              Weather
            </Link>

            <Link to="/report-incident" className="menu-item" onClick={closeMenu}>
              Report Incident
            </Link>

            {isAdmin && (
              <Link to="/admin-panel" className="menu-item" onClick={closeMenu}>
                Admin Panel
              </Link>
            )}

            {!isLoggedIn ? (
              <Link
                to="/login"
                className="menu-item login-item"
                onClick={closeMenu}
              >
                Login
              </Link>
            ) : (
              <button
                type="button"
                className="menu-item logout-item"
                onClick={handleLogout}
              >
                Logout
              </button>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;