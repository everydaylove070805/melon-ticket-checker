// webpack.config.js
module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: __dirname + '/dist',
  },
  mode: 'development', // 或 'production'
  module: {
    rules: [
      {
        test: /\.js$/, // 匹配所有 JavaScript 文件
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader', // 使用 babel-loader
          options: {
            presets: ['@babel/preset-env'], // 使用 @babel/preset-env 轉譯 JavaScript
          },
        },
      },
    ],
  },
};
