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
      'logo': ['Raleway', 'sans-serif']
    },
    fontSize: {
        'display': 82.6,
        'h1': 57.33,
        'h2': 47.77,
        'h3': 39.81,
        'h4': 33.17,
        'h5': 27.64,
        'h6': 23.04,
        'body-lg': 19.2,
        'body': 16,
        'body-sm': 13.33,
    },
    screens: {
      'mb': '375px',
      'dp': '768px',
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
}
