/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */

import nodeResolve from 'rollup-plugin-node-resolve';
import typescript from 'rollup-plugin-typescript2';
import babel from '@rollup/plugin-babel';
import json from '@rollup/plugin-json';
import { terser } from 'rollup-plugin-terser';
import commonjs from '@rollup/plugin-commonjs';

// import nodeResolve from 'rollup-plugin-node-resolve';
// import commonjs from '@rollup/plugin-commonjs';
// import typescript from 'rollup-plugin-typescript2';
// import babel from 'rollup-plugin-babel';
// import json from '@rollup/plugin-json';
// import summary from 'rollup-plugin-summary';
// import {terser} from 'rollup-plugin-terser';
// import resolve from '@rollup/plugin-node-resolve';
// import replace from '@rollup/plugin-replace';

const plugins = [
  nodeResolve(),
  commonjs({
    include: 'node_modules/**',
  }),
  typescript({
    include: ['src/**/*.ts'],
  }),
  json(),
  babel({
    babelHelpers: 'bundled',
    exclude: 'node_modules/**',
  }),
  terser(),
];

export default {
  input: 'src/smartknob-panel.ts',
  output: {
    dir: 'dist',
    format: 'iife',
    sourcemap: false,
  },
  onwarn(warning) {
    if (warning.code !== 'THIS_IS_UNDEFINED') {
      console.error(`(!) ${warning.message}`);
    }
  },
  plugins: plugins,
  context: 'window',
  // plugins: [
  //   replace({'Reflect.decorate': 'undefined'}),
  //   resolve(),
  //   /**
  //    * This minification setup serves the static site generation.
  //    * For bundling and minification, check the README.md file.
  //    */
  //   terser({
  //     ecma: 2021,
  //     module: true,
  //     warnings: true,
  //     mangle: {
  //       properties: {
  //         regex: /^__/,
  //       },
  //     },
  //   }),
  //   summary(),
  // ],
};
