import { PhoneCall } from "lucide-react";
import { emergencyContacts } from "../data/mockData.js";
import logo from "../ChatGPT.png";

export default function Footer() {
  return (
    <footer className="border-t border-slate-700 bg-slate-900">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 grid gap-8 md:grid-cols-2">
        <div>
          <div className="flex items-center gap-2 mb-3">
            <img src={logo} alt="PahadSuraksha logo" className="h-7 w-7 rounded object-cover" />
            <span className="font-bold text-white">PahadSuraksha</span>
          </div>
          <p className="text-sm text-slate-200">
            Helps drivers check weather and landslide risk before traveling mountain roads in Tehri Garhwal.
          </p>
        </div>

        <div>
          <p className="font-semibold text-white mb-3">Emergency Contacts</p>
          <ul className="space-y-2">
            {emergencyContacts.map((c) => (
              <li key={c.number} className="flex items-start gap-2 text-sm">
                <PhoneCall className="h-4 w-4 text-risk-high shrink-0 mt-0.5" />
                <div>
                  <span className="text-slate-200">{c.label}</span>
                  <span className="font-mono text-white ml-2">{c.number}</span>
                </div>
              </li>
            ))}
          </ul>
        </div>

      </div>
      <div className="border-t border-slate-700 py-4 text-center text-xs text-slate-300">
        © {new Date().getFullYear()} PahadSuraksha
      </div>
    </footer>
  );
}
