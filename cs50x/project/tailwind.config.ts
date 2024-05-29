import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      colors: {
        yellow: {
          1: "#FFA800",
          2: "#C28000",
        },
        blue: {
          1: "#6575A2",
          2: "#414B69",
        },
        black: {
          1: "#1E1E1E",
        },
        gray: {
          1: "#eee",
        },
      },
      fontFamily: {
        manrope: ["Manrope", "sans-serif"],
      },
      maxWidth: {
        "1012": "1012px",
      },
      height: {
        "1px": "1px",
        "90vh": "90vh",
      },
      width: {
        "1px": "1px",
      },
    },
  },
  plugins: [],
};
export default config;
