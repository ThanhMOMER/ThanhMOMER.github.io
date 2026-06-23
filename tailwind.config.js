/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html"],
  theme: {
    extend: {
      colors: {
        rescue: '#ffcc00', // Brighter neon yellow
        trust: '#3b82f6', // Brighter blue
        action: '#ff3333', // Neon red
        light: '#f8f9fa',
        darkbase: '#0f172a', // Slate 900
        darkcard: '#1e293b', // Slate 800
        neon: {
            red: '#ff2a2a',
            yellow: '#ffea00',
            blue: '#4facfe'
        }
      },
      fontFamily: {
        sans: ['"Be Vietnam Pro"', 'sans-serif'],
      },
      animation: {
        'float': 'float 3s ease-in-out infinite',
        'pulse-glow': 'pulseGlow 2s infinite',
        'slide-up': 'slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1)',
        'vibrate': 'vibrate 1.5s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        pulseGlow: {
          '0%, 100%': { opacity: 1, filter: 'drop-shadow(0 0 8px rgba(255, 51, 51, 0.6))' },
          '50%': { opacity: .7, filter: 'drop-shadow(0 0 15px rgba(255, 51, 51, 0.9))' },
        },
        slideUp: {
          '0%': { transform: 'translateY(100%)' },
          '100%': { transform: 'translateY(0)' },
        },
        vibrate: {
            '0%, 50%, 100%': { transform: 'translate(0)' },
            '10%, 30%': { transform: 'translate(-2px, 2px)' },
            '20%, 40%': { transform: 'translate(2px, -2px)' },
        }
      }
    },
  },
  plugins: [],
}
