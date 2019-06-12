const plugins = [
  '@babel/plugin-transform-runtime',
  'react-hot-loader/babel',
];

const presets = [
  '@babel/preset-react',
  [
    '@babel/preset-env',
    {
      useBuiltIns: 'usage',
      corejs: {
        version: 3,
        proposals: true,
      },
    },
  ],
];

module.exports = { presets, plugins };
