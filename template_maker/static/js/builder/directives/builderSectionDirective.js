(function() {
  'use strict';

  builder.directive('builderSection', [ function() {
    function link(scope, elem, attrs) {
      scope.rmElem = function() {
        scope.$destroy();
        elem.remove();
      };
    };

    return {
      restrict: 'AE',
      templateUrl: '../static/js/builder/partials/builder-section.html',
      link: link
    }
  }]);
})();