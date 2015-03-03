(function() {
  /*
    Most of the actual interaction with the content itself is housed
    in the controls directive. However, the each individual piece of content
    has its own scope so individual element-specific interactions
    are based in this directive
  */
  'use strict';

  builder.directive('builderContent', [ function() {
    function link(scope, elem, attrs) {
      scope.deleteElem = function(index) {
        scope.sections.splice(index, 1);
      }
    };

    return {
      restrict: 'AE',
      templateUrl: '../../static/js/builder/partials/builder-content.html',
      // This directive is interacting with another directive in the same
      // controller scope, so we set the transclude to true here.
      transclude: true,
      link: link
    }
  }]);
})();