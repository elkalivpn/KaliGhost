module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg-primary': '#0a0a0f',
        'bg-secondary': '#12121a',
        'bg-tertiary': '#1a1a2e',
        'accent-cyan': '#00ffff',
        'accent-purple': '#bf00ff',
        'accent-red': '#ff003c',
        'accent-green': '#00ff41',
        'text-primary': '#ffffff',
        'text-secondary': '#a0a0b0',
        'border-color': '#2a2a3e',
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      animation: {
        'pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce': 'bounce 1s infinite',
      },
    },
  },
  plugins: [],
}
