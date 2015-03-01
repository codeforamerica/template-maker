'use strict';

module.exports = function(grunt) {

  require('load-grunt-tasks')(grunt);

  grunt.initConfig({

    templateMaker: {
      js: './template_maker/static/js',
      lib: './template_maker/static/lib',
      test: './template_maker/static/test'
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
          'karma-spec-reporter'
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
      single: {
        singleRun: true,
        reporters: ['spec', 'coverage'],
        preprocessors: {
          '<%= templateMaker.js %>/**/*.js': ['coverage']
        },
        coverageReporter: {
          reporters: [
            { type: 'text' }
          ]
        }
      },
      continuous: {
        autowatch: true,
        singleRun: false,
        reporters: ['spec']
      },
      coverage: {
        singleRun: true,
        reporters: ['spec', 'coverage'],
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
    'karma:coverage'
  ]);

}