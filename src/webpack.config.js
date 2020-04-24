const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');

const isProduction = process.env.NODE_ENV === 'production';

const cssLoaders = [
  isProduction ? MiniCssExtractPlugin.loader : 'style-loader',
  {
    loader: 'css-loader',
    options: {
      modules: {
        auto: true,
      },
    },
  },
];

module.exports = {
  entry: './frontend/index.js',

  output: {
    path: path.resolve(__dirname, 'frontend-dist'),
    filename: '[name].[hash:6].js',
    chunkFilename: '[name].[hash:6].js',
    publicPath: '/',
  },

  mode: isProduction ? 'production' : 'development',

  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
      },
      {
        test: /\.css$/,
        use: cssLoaders,
      },
      {
        test: /\.less$/,
        use: [
          ...cssLoaders,
          {
            loader: 'less-loader',
            options: {
              lessOptions: {
                javascriptEnabled: true,
              },
            },
          },
        ],
      },
      {
        test: /\.(jpe?g|png|svg)$/,
        loader: 'file-loader',
      },
    ],
  },

  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'frontend'),
      '@components': path.resolve(__dirname, 'frontend/components'),
      '@pages': path.resolve(__dirname, 'frontend/pages'),
    },
  },

  plugins: [
    new HtmlWebpackPlugin({
      template: './frontend/index.html',
    }),

    new MiniCssExtractPlugin({
      filename: '[name].[hash:6].css',
    }),
  ],

  optimization: {
    minimizer: [new TerserPlugin(), new OptimizeCssAssetsPlugin()],
  },
};
