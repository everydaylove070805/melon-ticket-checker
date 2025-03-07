/** @type {import('eslint').Linter.Config} */
module.exports = [
  {
    // 直接加入你要繼承的配置
    parserOptions: {
      ecmaVersion: 2020,
      sourceType: "module",
    },
    rules: {
      "no-console": "warn",
    },
  },
  {
    // 如果你需要更多的共享配置，將它直接放在此處
    parserOptions: {
      ecmaVersion: "latest",
    },
  },
];
