/** @type {import('eslint').Linter.Config} */
module.exports = [
  {
    // 在平坦配置中直接引入擴展配置
    plugins: ["eslint-plugin"],
    rules: {
      "no-console": "warn",
    },
    languageOptions: {
      globals: {
        browser: true,
        node: true,
      },
    },
  },
  // 引入 eslint:recommended 配置
  {
    parserOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
    },
    rules: {
      "no-console": "warn",
    },
  },
];
