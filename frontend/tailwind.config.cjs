const flowbite = require('flowbite/plugin');
const forms = require('@tailwindcss/forms');

module.exports = {
  darkMode: 'class',
  content: [
    './src/**/*.{html,js,svelte,ts}',
    './node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}',
    './node_modules/flowbite/**/*.{js,ts}'
  ],
  theme: {
    extend: {}
  },
  plugins: [forms, flowbite]
};
