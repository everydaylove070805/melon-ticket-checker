const path = require('path');

module.exports = {
  entry: './src/index.js', // 你的入口文件
  output: {
    filename: 'bundle.js', // 輸出的文件名稱
    path: path.resolve(__dirname, 'dist') // 輸出文件的目錄
  },
  module: {
    rules: [
      {
        test: /\.js$/, // 處理所有 js 文件
        exclude: /node_modules/,
        use: 'babel-loader' // 使用 babel-loader 處理 JS 文件
      }
    ]
  },
  resolve: {
    extensions: ['.js'] // 設定支持的擴展名
  }
};
