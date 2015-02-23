(function() {
  'use strict';

  builder.directive('builderControls', ['$timeout', '$window', 
    function($timeout, $window) {
      function link(scope, elem, attrs) {
        scope.sections = [];

        scope.addTitle = function() {
          scope.sections.push({
            elem: 'input',
            type: 'text',
            _class: 'js-builder-title form-control',
            placeholder: 'Enter a title here',
            variables: [],
            content: ''
          });
        };

        scope.addSection = function() {
          scope.sections.push({
            elem: 'textarea',
            type: 'textarea',
            _class: 'js-builder-section form-control',
            placeholder: 'What is this section about?',
            variables: [],
            content: ''
          });
        };

        scope.addVariables = function() {

        };

        scope.saveTemplate = function() {
          scope.$emit('saveTemplate', scope.sections);
        }

        // add a hook to the scroll action to stick the
        // header to the top
        angular.element($window).bind('scroll', function() {
          var builderControlsElem = angular.element('.builder-controls');
          if (this.pageYOffset >= 20) {
            builderControlsElem.addClass('js-builder-controls-position-fixed');
          } else {
            builderControlsElem.removeClass('js-builder-controls-position-fixed');
          }
        })

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