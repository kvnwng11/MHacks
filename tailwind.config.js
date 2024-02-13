/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/*.{js,jsx,ts,tsx}",
    "./node_modules/tw-elements-react/dist/js/**/*.js"
  ],
  darkMode: "class",

  theme: {
    extend: {},
  },
  plugins: [require("tw-elements-react/dist/plugin.cjs")]
}

