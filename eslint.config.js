/** @type {import('eslint').Linter.Config} */
module.exports = {
  languageOptions: {
    globals: {
      browser: true,
      node: true,
    },
  },
  extends: 'eslint:recommended',
  rules: {
    'no-console': 'warn',
  },
};
