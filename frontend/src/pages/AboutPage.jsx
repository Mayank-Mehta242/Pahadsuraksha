import { Radar, ShieldCheck, Users } from "lucide-react";
import Card from "../components/Card.jsx";

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <p>About the platform</p>
      <h1 className="text-3xl font-display font-bold text-white mb-6">
        Built to give hill communities and travellers a head start
      </h1>
      <p className="text-slate-200 leading-relaxed mb-4">
        PahadSuraksha combines live weather data, terrain characteristics, and a historical record of landslide
        incidents across Uttarakhand into a single risk score for any point on the map. The goal is simple: give
        people a clear, explained answer to "is it safe to travel this route right now?" — before they set out,
        not after.
      </p>
      <p className="text-slate-200 leading-relaxed mb-10">
        The platform is designed for three audiences at once — everyday citizens checking conditions before a
        commute, tourists planning a mountain trip, and district disaster management teams who need an
        aggregated, district-wise view of emerging risk.
      </p>

      <div className="grid sm:grid-cols-3 gap-4">
        <Card>
          <Radar className="h-6 w-6 text-forest-500 mb-3" />
          <h3 className="font-semibold text-white mb-1.5 text-sm">AI-driven scoring</h3>
          <p className="text-xs text-slate-200 leading-relaxed">
            A Random Forest model weighs rainfall, slope, elevation, and history to produce an explained risk
            level.
          </p>
        </Card>
        <Card>
          <Users className="h-6 w-6 text-forest-500 mb-3" />
          <h3 className="font-semibold text-white mb-1.5 text-sm">Community reporting</h3>
          <p className="text-xs text-slate-200 leading-relaxed">
            Citizens can report incidents directly, feeding a moderated stream back into the map.
          </p>
        </Card>
        <Card>
          <ShieldCheck className="h-6 w-6 text-forest-500 mb-3" />
          <h3 className="font-semibold text-white mb-1.5 text-sm">Actionable guidance</h3>
          <p className="text-xs text-slate-200 leading-relaxed">
            Every risk level comes with concrete safety guidance, not just a number.
          </p>
        </Card>
      </div>
    </div>
  );
}
