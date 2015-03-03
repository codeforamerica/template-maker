(function() {
  /*

  */
  'use strict';

  builder.controller('templateListCtrl', ['$scope', 'builderSubmit',
    function($scope, builderSubmit) {

      $scope.deleteTemplate = function(templateId) {
        if(confirm('Are you sure you want to delete this template?')) {
          builderSubmit.deleteTemplate(templateId).then(function(templateId) {
            var elem = angular.element('#template-' + templateId);
            elem.remove();
          });
        }
      }

    }
  ]);
})();
