(function() {
  'use strict';

  builder.directive('setfocus', [ function() {
    return {
      restrict: 'A',
      scope: {
        setfocus: '='
      },
      link: function(scope, elem, attrs) {
        if (scope.setfocus === true) {
          elem[0].focus();
        }
      }
    }
  }]);
})();