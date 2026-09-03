import { NavLink, Outlet } from "react-router-dom";
import {
  Map,
  AlertTriangle,
  FlagTriangleRight,
  UserRound,
} from "lucide-react";
import Navbar from "../components/Navbar.jsx";

const SIDEBAR_LINKS = [
  { label: "Map", to: "/dashboard", icon: Map },
  { label: "Check Risk", to: "/dashboard/risk", icon: AlertTriangle },
  { label: "Report Incident", to: "/report-incident", icon: FlagTriangleRight },
  { label: "Account", to: "/account", icon: UserRound },
];

export default function DashboardLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 flex">
        <aside className="hidden lg:flex flex-col w-56 shrink-0 border-r border-slate-700/80 bg-slate-900/95 backdrop-blur px-4 py-6 gap-1">
          {SIDEBAR_LINKS.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.to === "/dashboard"}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                  isActive ? "bg-forest-600 text-white shadow-md shadow-forest-600/25" : "text-slate-300 hover:text-slate-100 hover:bg-slate-800/80"
                }`
              }
            >
              <link.icon className="h-4 w-4" />
              {link.label}
            </NavLink>
          ))}
        </aside>
        <main className="flex-1 min-w-0 contour-surface px-4 sm:px-6 lg:px-10 py-8 lg:py-10">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
