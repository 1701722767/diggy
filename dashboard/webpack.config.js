// const SpeedMeasurePlugin = require('speed-measure-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
// const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  entry: 'index.js',
  output: {
    path: __dirname + '/dist',
    filename: 'index_bundle.js'
  },
  plugins: [new HtmlWebpackPlugin(),new MiniCssExtractPlugin()],
};

// const configWithTimeMeasures = new SpeedMeasurePlugin().wrap(config);
// configWithTimeMeasures.plugins.push(new MiniCssExtractPlugin({}));

// module.exports = configWithTimeMeasures;