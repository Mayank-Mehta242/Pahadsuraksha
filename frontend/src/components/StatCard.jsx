export default function StatCard({ icon: Icon, value, label }) {
  return (
    <div className="glass-panel p-6 flex items-center gap-4">
      <div className="h-12 w-12 rounded-full bg-forest-800/60 border border-forest-600/40 flex items-center justify-center shrink-0">
        <Icon className="h-6 w-6 text-forest-500" strokeWidth={1.75} />
      </div>
      <div>
        <p className="text-2xl font-display font-bold text-slate-50">{value}</p>
        <p className="text-sm text-slate-400">{label}</p>
      </div>
    </div>
  );
}
