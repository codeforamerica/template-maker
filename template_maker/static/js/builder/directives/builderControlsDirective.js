(function() {
  'use strict';

  builder.directive('builderControls', ['$compile', function($compile) {
    function link(scope, elem, attrs) {

      var contentElem = angular.element(scope.target);

      scope.addTitle = function() {
        var newScope = scope.$new();
        contentElem.append($compile('<builder-title></builder-title>')(newScope));
      }

      scope.addSection = function() {
        var newScope = scope.$new();
        contentElem.append($compile('<builder-section></builder-section>')(newScope));
      }

      scope.addVariables = function() {

      }

    };

    return {
      restrict: 'AE',
      templateUrl: '../static/js/builder/partials/builder-controls.html',
      scope: {
        target: '=',
      },
      link: link
    };

  }]);

})();