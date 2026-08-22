import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Tooltip, Legend, Filler);

export const chartTextColor = "#AEBBB4";
export const chartGridColor = "rgba(255,255,255,0.06)";

export const baseChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { labels: { color: chartTextColor, font: { family: "Manrope" } } },
    tooltip: { backgroundColor: "#131A17", borderColor: "rgba(255,255,255,0.1)", borderWidth: 1 },
  },
  scales: {
    x: { ticks: { color: chartTextColor }, grid: { color: "transparent" } },
    y: { ticks: { color: chartTextColor }, grid: { color: chartGridColor } },
  },
};
