'use strict';

module.exports = function(grunt) {

  require('load-grunt-tasks')(grunt);

  grunt.initConfig({

    templateMaker: {
      js: './template_maker/static/js',
      lib: './template_maker/static/lib',
      test: './template_maker/static/test',
      thresholds: {
        statements: 90,
        branches: 60,
        functions: 85,
        lines: 90
      }
    },

    karma: {
      options: {
        basePath: '.',
        browsers: ['PhantomJS'],
        frameworks: [
          'mocha',
          'chai',
          'sinon'
        ],
        plugins: [
          'karma-chai',
          'karma-coverage',
          'karma-mocha',
          'karma-phantomjs-launcher',
          'karma-sinon',
          'karma-spec-reporter',
          'karma-threshold-reporter'
        ],
        files: [
          // framework files
          '<%= templateMaker.lib %>/angular/angular.js',
          '<%= templateMaker.lib %>/angular-mocks/angular-mocks.js',
          '<%= templateMaker.lib %>/angular-sanitize/angular-sanitize.js',
          '<%= templateMaker.lib %>/angular-sanitize/angular-sanitize.js',
          // app files
          '<%= templateMaker.js %>/**/*.js',
          // test files
          '<%= templateMaker.test %>/unit/**/*.js',
        ]
      },
      simple: {
        singleRun: true,
        reporters: ['spec']
      },
      single: {
        singleRun: true,
        reporters: ['spec', 'coverage', 'threshold'],
        thresholdReporter: {
          statements: '<%= templateMaker.thresholds.statements %>',
          branches: '<%= templateMaker.thresholds.branches %>',
          functions: '<%= templateMaker.thresholds.functions %>',
          lines: '<%= templateMaker.thresholds.lines %>',
        },
        preprocessors: {
          '<%= templateMaker.js %>/**/*.js': ['coverage']
        },
        coverageReporter: {
          reporters: []
        }
      },
      continuous: {
        autowatch: true,
        singleRun: false,
        reporters: ['spec']
      },
      coverage: {
        singleRun: true,
        reporters: ['spec', 'coverage', 'threshold'],
        thresholdReporter: {
          statements: '<%= templateMaker.thresholds.statements %>',
          branches: '<%= templateMaker.thresholds.branches %>',
          functions: '<%= templateMaker.thresholds.functions %>',
          lines: '<%= templateMaker.thresholds.lines %>',
        },
        preprocessors: {
          '<%= templateMaker.js %>/**/*.js': ['coverage']
        },
        coverageReporter: {
          reporters: [
            { type: 'html', dir: 'coverage-js' }
          ]
        }
      }
    }

  });

  grunt.registerTask('test:unit', [
    'karma:single'
  ]);

}