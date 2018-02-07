module.exports = {
  entry: [
    './app/photogallery.scss',
    './app/photogallery.js',
    './app/photogallery_icon.png',
    './app/tile-photogallery.png',
  ],
  output: {
    filename: 'photogallery.js',
    library: 'photogallery',
    libraryTarget: 'umd',
    path: __dirname + '/../src/sc/photogallery/browser/static',
    publicPath: '++theme++sc.photogallery/'
  },
  module: {
    rules: [{
      test: /\.js$/,
      exclude: /(\/node_modules\/|test\.js$|\.spec\.js$)/,
      use: 'babel-loader',
    }, {
      test: /\.scss$/,
      use: [
        {
          loader: 'file-loader',
          options: {
            name: '[name].css',
          }
        },
        'extract-loader',
        'css-loader',
        'postcss-loader',
        'sass-loader'
      ]
    }, {
      test: /.*\.(gif|png|jpe?g)$/i,
      use: [
        {
          loader: 'file-loader',
          options: {
            name: '[path][name].[ext]',
            context: 'app/'
          }
        },
        {
          loader: 'image-webpack-loader',
          query: {
            mozjpeg: {
              progressive: true,
            },
            pngquant: {
              quality: '65-90',
              speed: 4
            },
            gifsicle: {
              interlaced: false
            },
            optipng: {
              optimizationLevel: 7
            }
          }
        }
      ]
    }]
  },
  devtool: 'source-map'
}
