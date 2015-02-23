(function() {
  'use strict';

  builder.directive('builderControls', ['$timeout', '$compile', 
    function($timeout, $compile) {
      function link(scope, elem, attrs) {
        scope.sections = [];

        function focusCursor(element) {
          if (scope.setFocus === true) {
            element[0].focus();
          }
        }

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
          focusCursor(elem);
        };

        scope.addVariables = function() {

        };

        scope.saveTemplate = function() {
          scope.$emit('saveTemplate', scope.sections);
        }

      };

      return {
        restrict: 'AE',
        templateUrl: '../static/js/builder/partials/builder-controls.html',
        transclude: true,
        link: link
      };
    }
  ]);

})();