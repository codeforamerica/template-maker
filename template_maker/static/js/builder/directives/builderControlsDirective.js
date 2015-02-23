(function() {
  'use strict';

  builder.directive('builderControls', ['$compile', function($compile) {
    function link(scope, elem, attrs) {
      scope.sections = [];

      scope.addTitle = function() {
        scope.sections.push({
          elem: 'input',
          type: 'text',
          _class: 'js-builder-title form-control',
          variables: [],
          content: ''
        });
      };

      scope.addSection = function() {
        scope.sections.push({
          elem: 'textarea',
          type: 'textarea',
          _class: 'js-builder-section form-control',
          variables: [],
          content: ''
        });
      };

      scope.addVariables = function() {

      };

    };

    return {
      restrict: 'AE',
      templateUrl: '../static/js/builder/partials/builder-controls.html',
      transclude: true,
      link: link
    };

  }]);

})();