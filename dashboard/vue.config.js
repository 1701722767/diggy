const { defineConfig } = require("@vue/cli-service");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = defineConfig({
  transpileDependencies: ["vuetify"],
  lintOnSave: false,
  configureWebpack: {
    plugins: [new MiniCssExtractPlugin()],
  },
});
