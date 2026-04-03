/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        accent: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e', // Vibrant green from image
          600: '#16a34a',
          700: '#15803d',
        },
        surface: {
          900: '#111111', // Main background
          800: '#1E1E1E', // Sidebar background
          700: '#2D2D2D', // Card hover
          600: '#3A3A3A', // Input background
        }
      },
    },
  },
  plugins: [],
}