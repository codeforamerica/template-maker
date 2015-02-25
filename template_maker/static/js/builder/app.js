var builder = angular.module('builder', []);

builder.config(['$interpolateProvider', '$httpProvider',
  function($interpolateProvier, $httpProvider) {
    $interpolateProvier.startSymbol('{[');
    $interpolateProvier.endSymbol(']}');

    // add X-Requested-With header to all angular requests
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  }
]);