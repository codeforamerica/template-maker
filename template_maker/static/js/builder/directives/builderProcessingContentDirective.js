(function() {
  /*
    This directive is responsible for handling all styling of the actual
    content in the template and rendering it to the DOM.
  */
  'use strict';

  builder.directive('templateContent', ['$timeout', '$compile', 'formatHtml',
    function($timeout, $compile, formatHtml) {
      function link(scope, elem, attrs) {

        scope.formattedContent = [];
        $timeout(function() {
          scope.content.forEach(function(section) {
            scope.formattedContent.push({
              type: section.type,
              content: formatHtml.generateSectionHtml(section)
            })
          });
        });

      }

      return {
        restrict: 'E',
        templateUrl: '../../../static/js/builder/partials/processing-content.html',
        transclude: true,
        scope: {
          content: '='
        },
        link: link
      }
    }
  ])
})();
