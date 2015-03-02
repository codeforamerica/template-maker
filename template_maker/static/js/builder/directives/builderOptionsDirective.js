(function() {
  /*
    Setfocus is a custom attribute directive that causes 
    input fields to autofocus when they are added.
  */
  'use strict';

  builder.directive('builderOptions', [ function() {
    return {
      restrict: 'A',
      scope: {
        setfocus: '=',
        editable: '='
      },
      link: function(scope, elem, attrs) {

        if (scope.setfocus === true) {
          elem[0].focus();
        };

      }
    }
  }]);
})();