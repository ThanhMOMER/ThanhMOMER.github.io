/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html"],
  theme: {
    extend: {
      colors: {
        rescue: '#ffc107',
        trust: '#1e3a8a',
        action: '#dc2626',
        light: '#f8f9fa',
      },
      fontFamily: {
        sans: ['"Be Vietnam Pro"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
