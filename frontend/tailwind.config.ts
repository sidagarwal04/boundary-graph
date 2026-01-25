/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue",
  ],
  theme: {
    screens: {
      'xs': '475px',
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
    },
    extend: {
      colors: {
        brand: {
          dark: '#0B1120',   // Almost Black
          primary: '#1E3A8A', // IPL Royal Blue
          secondary: '#475569', // Slate
          accent: '#F97316',  // IPL Orange
          success: '#10B981',
          warning: '#F59E0B',
          danger: '#EF4444',
          gold: '#FFD700',    // IPL Gold
          purple: '#7C3AED',  // IPL Purple
        },
        ipl: {
          blue: '#1E3A8A',    // IPL Primary Blue
          orange: '#F97316',   // IPL Orange
          gold: '#FFD700',     // IPL Gold
          purple: '#7C3AED',   // IPL Purple
          'blue-dark': '#1E40AF',
          'blue-light': '#3B82F6',
        },
        teams: {
          // IPL Team Colors
          csk: '#FFFF00',      // Chennai Super Kings - Yellow
          dc: '#004C93',       // Delhi Capitals - Blue
          gt: '#1C4E80',       // Gujarat Titans - Dark Blue
          kkr: '#3A225D',      // Kolkata Knight Riders - Purple
          lsg: '#00A7CC',      // Lucknow Super Giants - Light Blue
          mi: '#004BA0',       // Mumbai Indians - Blue
          pk: '#ED1B24',       // Punjab Kings - Red
          rr: '#254AA5',       // Rajasthan Royals - Pink/Blue
          rcb: '#D50000',      // Royal Challengers Bengaluru - Red
          srh: '#F26522',      // Sunrisers Hyderabad - Orange
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s infinite',
        'bounce-light': 'bounce 2s infinite',
        'gradient': 'gradient 6s ease infinite',
        'shimmer': 'shimmer 2s infinite linear',
      },
      keyframes: {
        gradient: {
          '0%, 100%': { 'background-position': '0% 50%' },
          '50%': { 'background-position': '100% 50%' },
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
      },
      backgroundImage: {
        'gradient-ipl': 'linear-gradient(135deg, #1E3A8A 0%, #F97316 100%)',
        'gradient-gold': 'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)',
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      },
      spacing: {
        'safe-top': 'env(safe-area-inset-top)',
        'safe-bottom': 'env(safe-area-inset-bottom)',
        'safe-left': 'env(safe-area-inset-left)',
        'safe-right': 'env(safe-area-inset-right)',
      },
      minHeight: {
        'touch': '44px',
      },
      minWidth: {
        'touch': '44px',
      }
    },
  },
  plugins: [],
}
