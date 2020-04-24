const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const isProduction = process.env.NODE_ENV === 'production';

module.exports = {
  entry: './frontend/index.js',

  output: {
    path: path.resolve(__dirname, 'frontend-dist'),
    filename: '[name].[hash:6].js',
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
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              modules: {
                auto: true,
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
  ],
};
