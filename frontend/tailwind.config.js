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
        background: {
          950: '#030712',
          900: '#0f172a', // Deep slate/indigo
          800: '#1e293b',
        },
        accent: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          200: '#99f6e4',
          300: '#5eead4',
          400: '#2dd4bf',
          500: '#14b8a6', // Soft Teal
          600: '#0d9488',
          700: '#0f766e',
          800: '#115e59',
          900: '#134e4a',
        },
        surface: {
          900: '#0f172a',
          800: '#1e293b',
          700: '#334155',
          600: '#475569',
        },
        emotion: {
            joy: '#fbbf24',
            sadness: '#60a5fa',
            anger: '#f87171',
            fear: '#a78bfa',
            neutral: '#94a3b8',
            caring: '#f472b6'
        }
      },
      backgroundImage: {
        'glass-gradient': 'linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%)',
        'zen-radial': 'radial-gradient(circle at center, #1e293b 0%, #030712 100%)',
      }
    },
  },
  plugins: [],
}