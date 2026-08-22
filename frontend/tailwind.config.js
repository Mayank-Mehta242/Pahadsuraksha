/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        slate: {
          950: "#1b241c",
          900: "#263126",
          800: "#344233",
          700: "#4e5a47",
          600: "#64705b",
          500: "#818d78",
          400: "#a5b09f",
          300: "#c4cdbd",
          200: "#dce4d6",
          100: "#edf2e9",
          50: "#f6f8f3",
        },
        forest: {
          600: "#1E8354",
          500: "#2A9D6B",
        },
        risk: {
          low: "#22A567",
          medium: "#E0B324",
          high: "#E07A24",
          extreme: "#C7362B",
        },
      },
      fontFamily: {
        display: ["system-ui", "sans-serif"],
        body: ["system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
