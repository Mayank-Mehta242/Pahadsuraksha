import { Bell, MapPin, Search, UserRound } from "lucide-react";
import Card from "../components/Card.jsx";
import { useAuth } from "../hooks/useAuth.js";

const savedLocations = ["Chamoli", "Uttarkashi"];
const recentSearches = ["Joshimath", "Kedarnath route"];
const notifications = [
  { id: 1, text: "Risk upgraded to HIGH near Chamoli.", time: "2h ago" },
  { id: 2, text: "Your incident report was approved.", time: "1d ago" },
];

export default function UserAccountPage() {
  const { user } = useAuth();

  return (
    <div>
      <div className="flex items-center gap-4 mb-8">
        <div className="h-12 w-12 rounded-full bg-forest-600/30 border border-forest-600 flex items-center justify-center">
          <UserRound className="h-6 w-6 text-forest-500" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-white">{user?.name}</h1>
          <p className="text-sm text-slate-200">
            {user?.email} • {user?.district}
          </p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <Card title="Saved Locations" action={<MapPin className="h-4 w-4 text-slate-500" />}>
          <ul className="space-y-2">
            {savedLocations.map((l) => (
              <li key={l} className="text-sm text-white bg-slate-800 rounded px-3 py-2">
                {l}
              </li>
            ))}
          </ul>
        </Card>

        <Card title="Recent Searches" action={<Search className="h-4 w-4 text-slate-500" />}>
          <ul className="space-y-2">
            {recentSearches.map((s) => (
              <li key={s} className="text-sm text-white bg-slate-800 rounded px-3 py-2">
                {s}
              </li>
            ))}
          </ul>
        </Card>

        <Card title="Alerts" action={<Bell className="h-4 w-4 text-slate-500" />}>
          <ul className="space-y-3">
            {notifications.map((n) => (
              <li key={n.id} className="text-sm">
                <p className="text-slate-100">{n.text}</p>
                <p className="text-xs text-slate-300 mt-1">{n.time}</p>
              </li>
            ))}
          </ul>
        </Card>

        <Card title="About You">
          <p className="text-sm text-slate-200 mb-3">
            Update your profile or manage your saved preferences here.
          </p>
          <p className="text-xs text-slate-300">Feature coming soon</p>
        </Card>
      </div>
    </div>
  );
}
