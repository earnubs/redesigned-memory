const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const TerserJSPlugin = require('terser-webpack-plugin');

module.exports = ({ mode }) => {

  const isDev = (mode !== 'production');

  return {
    mode,
    entry: './src/index.js',
    devServer: {
      contentBase: './dist',
      host: '0.0.0.0',
      port: 3000,
      proxy: {
        '/api': 'http://localhost:8000',
      },
    },
    optimization: {
      minimizer: [new TerserJSPlugin({}), new OptimizeCSSAssetsPlugin({})],
    },
    plugins: [
      new HtmlWebpackPlugin({
        title: 'Development',
        template: 'src/index.html',
      }),
      new MiniCssExtractPlugin({
        filename: isDev ? '[name].css' : '[name].[hash].css',
        chunkFilename: isDev ? '[id].css' : '[id].[hash].css',
      }),
    ],
    stats: {
      all: false,
      assets: true,
      builtAt: true,
      errorDetails: true,
      errors: true,
      performance: true,
    },
    module: {
      rules: [
        {
          test: /\.m?js$/,
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-env'],
            },
          },
        },
        {
          test: /\.css$/,
          use: [{
            loader: MiniCssExtractPlugin.loader,
            options: {
              hmr: isDev,
            },
          },
          'css-loader',
          'postcss-loader',
          ],
        },
      ],
    },
    output: {
      filename: isDev ? '[name].bundle.js' : '[name].[contenthash].js',
      path: path.resolve(__dirname, 'dist'),
    },
  };
};
