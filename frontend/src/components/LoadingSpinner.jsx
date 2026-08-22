export default function LoadingSpinner({ label = "Loading" }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-12 text-slate-400">
      <div className="h-9 w-9 rounded-full border-2 border-forest-600 border-t-transparent animate-spin" />
      <p className="text-sm">{label}…</p>
    </div>
  );
}
