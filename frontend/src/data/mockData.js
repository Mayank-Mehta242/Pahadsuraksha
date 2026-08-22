// Mock data for development
// In production, this is replaced by API calls when VITE_USE_MOCK_DATA=false

export const mockDistricts = [
  { id: "tehri-garhwal", name: "Tehri Garhwal", lat: 30.3752, lng: 78.48, risk: "medium", incidents: 12 },
];

export const mockStats = {
  monitoredDistricts: 1,
  reportedIncidents: 56,
  activeUsers: 234,
};

export const mockHistorical = {
  monthly: [
    { month: "Apr", count: 8 },
    { month: "May", count: 11 },
    { month: "Jun", count: 15 },
    { month: "Jul", count: 22 },
  ],
  yearly: [
    { year: 2024, count: 42 },
    { year: 2025, count: 51 },
    { year: 2026, count: 56 },
  ],
  topVulnerable: ["Tehri Garhwal"],
};

export const mockWeather = {
  location: "Tehri Garhwal",
  temperatureC: 14,
  humidityPct: 75,
  rainfallMm: 35,
  windKmh: 16,
  elevationM: 1950,
  condition: "Moderate Rain",
  forecast: [
    { day: "Mon", tempC: 14, rainMm: 35, humidityPct: 75 },
    { day: "Tue", tempC: 13, rainMm: 45, humidityPct: 80 },
    { day: "Wed", tempC: 15, rainMm: 25, humidityPct: 70 },
  ],
};

export const mockPredictionResult = {
  riskLevel: "HIGH",
  confidence: 87,
  reasons: [
    "Heavy rainfall over past 48 hours",
    "Steep terrain in this area",
    "Historical incidents nearby",
  ],
  factorWeights: [
    { factor: "Rainfall", weight: 0.35 },
    { factor: "Slope", weight: 0.30 },
    { factor: "Historical incidents", weight: 0.25 },
    { factor: "Humidity", weight: 0.10 },
  ],
};

export const mockReports = [
  {
    id: "r1",
    title: "Debris on Badrinath highway near Pipalkoti",
    district: "Chamoli",
    lat: 30.28,
    lng: 79.35,
    status: "approved",
    createdAt: "2026-07-21",
  },
  {
    id: "r2",
    title: "Minor slope slippage above Joshimath",
    district: "Chamoli",
    lat: 30.56,
    lng: 79.57,
    status: "pending",
    createdAt: "2026-07-25",
  },
];

export const emergencyContacts = [
  { label: "Uttarakhand Disaster Helpline", number: "1070" },
  { label: "National Emergency", number: "112" },
  { label: "Ambulance", number: "108" },
];
