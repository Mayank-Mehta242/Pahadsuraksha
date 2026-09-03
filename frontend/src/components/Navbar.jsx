import { useState } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { Menu, X, User } from "lucide-react";
import { NAV_LINKS } from "../utils/constants.js";
import { useAuth } from "../hooks/useAuth.js";
import logo from "../ChatGPT.png";

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const links = user?.role === "district_officer"
    ? [...NAV_LINKS, { label: "Approvals", to: "/admin" }]
    : NAV_LINKS;

  return (
    <header className="sticky top-0 z-40 border-b border-slate-700/80 bg-[#142016]/95 backdrop-blur">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 md:h-[4.5rem] flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 shrink-0">
          <img src={logo} alt="PahadSuraksha logo" className="h-8 w-8 rounded object-cover" />
          <span className="font-display font-bold text-lg text-slate-100">
            PahadSuraksha
          </span>
        </Link>

        <div className="hidden md:flex items-center gap-3">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `px-3 py-2 text-sm rounded-xl transition-all duration-200 ${
                  isActive ? "text-forest-500 bg-forest-500/15" : "text-slate-300 hover:text-slate-100 hover:bg-slate-800/70"
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </div>

        <div className="hidden md:flex items-center gap-3">
          {user ? (
            <>
              <span className="text-sm text-slate-400">{user.name}</span>
              <button
                onClick={() => {
                  logout();
                  navigate("/");
                }}
                className="btn-secondary text-sm"
              >
                Log out
              </button>
            </>
          ) : (
            <Link to="/login" className="btn-primary text-sm">
              Login
            </Link>
          )}
        </div>

        <button className="md:hidden text-slate-300 transition-colors hover:text-white" onClick={() => setOpen((o) => !o)} aria-label="Toggle menu">
          {open ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </nav>

      {open && (
        <div className="md:hidden border-t border-slate-700 bg-[#1d2a1d] px-4 py-4 space-y-2">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `block px-3 py-2.5 rounded-xl text-sm transition-all duration-200 ${
                  isActive ? "text-forest-500 bg-forest-500/15" : "text-slate-300 hover:text-slate-100 hover:bg-slate-800/70"
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}
          <div className="pt-2 border-t border-slate-700">
            {user ? (
              <button
                onClick={() => {
                  logout();
                  setOpen(false);
                  navigate("/");
                }}
                className="btn-secondary w-full text-sm mt-2"
              >
                Log out
              </button>
            ) : (
              <Link to="/login" onClick={() => setOpen(false)} className="btn-primary w-full text-sm block text-center">
                Login
              </Link>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
