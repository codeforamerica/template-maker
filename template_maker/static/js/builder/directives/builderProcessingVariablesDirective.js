(function() {
  /*
    This directive is responsible for handling the styling and
    DOM rendering around the variable box in the processing stage
   */
  'use strict'

  builder.directive('templateVariables', [ (function() {
    function link(scope, elem, attrs) {
      scope.dataTypes = [
        { 'type': 'unicode', 'display': 'Text' },
        { 'type': 'date', 'display': 'Date' },
        { 'type': 'int', 'display': 'Integer' },
        { 'type': 'float', 'display': 'Decimal' }
      ];
    }

    return {
      restrict: 'E',
      templateUrl: '../../../static/js/builder/partials/processing-variables.html',
      transclude: true,
      scope: {
        variables: '='
      },
      link: link
    }
  })])
})();
