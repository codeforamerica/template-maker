(function() {
  /*
    This directive is responsible for handling all styling of the actual
    content in the template and rendering it to the DOM.
  */
  'use strict';

  builder.directive('templateContent', ['$timeout', '$compile',
    function($timeout, $compile) {
      function link(scope, elem, attrs) {
        function highlightVariables(contentText) {
          // TOOD: There has to be a better way to do this.
          var variableRegex = /({{ |{{).*?(}}| }})/g
          var toHighlight = contentText.match(variableRegex);
          var toHighlightTmp = {}, 
            highlightedTmp = {},
            highlightedFinal = [],
            toHighlightFinal = [];

          if (toHighlight === null) { return contentText; }

          toHighlight.forEach(function(text) {
            toHighlightTmp[text] = '';
            highlightedTmp['<span class="js-processing-highighted">' + text + "</span>"] = '';
          });

          for (var item in toHighlightTmp) {
            toHighlightFinal.push(item);
          }

          for (var item in highlightedTmp) {
            highlightedFinal.push(item);
          }

          for (var i=0; i<highlightedFinal.length; i++) {
            var find = toHighlightFinal[i];
            var re = new RegExp(find, 'g');
            contentText = contentText.replace(re, highlightedFinal[i]);
          }

          return contentText;
        }

        scope.formattedContent = [];

        $timeout(function() {
          scope.content.forEach(function(section) {
            scope.formattedContent.push({
              type: section.type,
              content: highlightVariables(section.content)
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