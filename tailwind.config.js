/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/*.html",
            "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {
      colors: {
        chatblack: {50: "#343541"},
        chathist: {100: "#202123"},
        cardbutton: {200: "#3e3f4b"},
        text_red: {300: "#fe0a44"}
      },
      backgroundImage: {
        'service-pattern': "url('app/static/assets/dotted.svg')"
        // 'footer-texture': "url('/img/footer-texture.png')"
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}
}

