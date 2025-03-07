/** @type {import('eslint').Linter.Config} */
module.exports = {
  env: {
    browser: true,
    node: true
  },
  extends: "eslint:recommended",
  rules: {
    "no-console": "warn"
  }
};
