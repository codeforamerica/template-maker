(function() {
  /*
   While the majority of the functionality and layout for this view
   is controlled by the backend/flask portion of the builder, the DELETE
   method is handled here.
  */
  'use strict';

  builder.controller('templateListCtrl', ['$scope', '$window', 'builderSubmit',
    function($scope, $window, builderSubmit) {

      $scope.deleteTemplate = function(templateId) {
        var answer = $window.confirm('Are you sure you want to delete this template?');
        if(answer) {
          builderSubmit.deleteTemplate(templateId).then(function(templateId) {
            var elem = angular.element('#template-' + templateId);
            elem.remove();
          });
        }
      }

    }
  ]);
})();
