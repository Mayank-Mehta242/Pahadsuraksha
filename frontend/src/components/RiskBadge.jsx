import { RISK_STYLES, normalizeRiskKey } from "../utils/riskUtils.js";

export default function RiskBadge({ level, size = "md" }) {
  const key = normalizeRiskKey(level);
  const style = RISK_STYLES[key];
  const sizeClasses = size === "lg" ? "px-4 py-2 text-sm" : "px-3 py-1 text-xs";

  return (
    <span
      className={`inline-flex items-center gap-2 rounded-full border ${style.border} ${style.bg} ${style.text} ${sizeClasses} font-semibold uppercase tracking-wide`}
    >
      <span className={`h-2 w-2 rounded-full ${style.dot}`} />
      {style.label}
    </span>
  );
}
