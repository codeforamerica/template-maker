var builder = angular.module('builder', []);

builder.config(['$interpolateProvider',
  function($interpolateProvier) {
    $interpolateProvier.startSymbol('{[');
    $interpolateProvier.endSymbol(']}');
  }
]);