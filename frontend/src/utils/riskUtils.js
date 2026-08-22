export const RISK_STYLES = {
  low: { label: "Low", dot: "bg-risk-low", text: "text-risk-low", bg: "bg-risk-low/15", border: "border-risk-low/40" },
  medium: {
    label: "Medium",
    dot: "bg-risk-medium",
    text: "text-risk-medium",
    bg: "bg-risk-medium/15",
    border: "border-risk-medium/40",
  },
  high: {
    label: "High",
    dot: "bg-risk-high",
    text: "text-risk-high",
    bg: "bg-risk-high/15",
    border: "border-risk-high/40",
  },
  extreme: {
    label: "Very High",
    dot: "bg-risk-extreme",
    text: "text-risk-extreme",
    bg: "bg-risk-extreme/15",
    border: "border-risk-extreme/40",
  },
};

export function normalizeRiskKey(level) {
  const key = String(level).toLowerCase();
  if (key.includes("very") || key.includes("extreme")) return "extreme";
  if (key.includes("high")) return "high";
  if (key.includes("med")) return "medium";
  return "low";
}
