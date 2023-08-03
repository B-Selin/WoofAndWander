/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}"],
  theme: {
    colors: {
      'primary': '#D7837F',
      'secondary': '#F2C487',
      'accent': '#57A8AC',
      'dark': '#1B0A0A',
      'light': '#FAEEED'
    },
    fontFamily: {
      'header': ['Libre Baskerville', 'serif'],
      'body': ['Montserrat', 'sans-serif'],
    },
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
}

