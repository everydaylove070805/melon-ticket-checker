/** @type {import('eslint').Linter.Config} */
module.exports = [
  {
    // 將 plugins 改為物件格式
    plugins: {
      "eslint-plugin": require("eslint-plugin"), // 這是插件的實際引入
    },
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
];
