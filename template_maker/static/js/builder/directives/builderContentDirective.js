(function() {
  'use strict';

  builder.directive('builderContent', [ function() {
    function link(scope, elem, attrs) {
      scope.deleteElem = function(index) {
        scope.sections.splice(index, 1);
      }
    };

    return {
      restrict: 'AE',
      templateUrl: '../static/js/builder/partials/builder-content.html',
      transclude: true,
      link: link
    }
  }]);
})();