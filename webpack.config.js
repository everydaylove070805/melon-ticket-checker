// webpack.config.js
module.exports = {
  entry: './src/index.js', // 設定入口點
  output: {
    filename: 'bundle.js', // 設定輸出文件名
    path: __dirname + '/dist', // 輸出目錄
  },
  mode: 'development', // 設定 mode，開發模式
};
