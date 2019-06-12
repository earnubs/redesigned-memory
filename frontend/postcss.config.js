const postcssPresetEnv = require('postcss-preset-env');

module.exports = {
  map: true,
  plugins: [
    postcssPresetEnv(),
  ],
};
