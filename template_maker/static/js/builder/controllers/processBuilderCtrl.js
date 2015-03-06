(function() {
  /*
   The processBuilderCtrl is the controller that surrounds
   the variable editing portion of the template generation
   process
   */
  'use strict';

  builder.controller('processBuilderCtrl', ['$scope', '$location', 'builderGetData', 'messageBus', 'builderSubmit', 'builderLocationHandler',
    function($scope, $location, builderGetData, messageBus, builderSubmit, builderLocationHandler) {
      // try to get the id from the messages
      // otherwise get it from the url
      $scope.templateId = messageBus.pop();
      if ($scope.templateId === null) {
        var urlParts = $location.absUrl().split('/');
        $scope.templateId = urlParts[urlParts.length - 2];
      }

      builderGetData.getData('/build/data/templates/' + $scope.templateId + '/process').then(function(data) {
        $scope.content = data.template;
        // extract and flatten the variable names from each section
        $scope.variables = data.template.map(function(datum) {
          return datum.variables.map(function(variable) {
            return {
              variable: variable,
              type: '',
              error: false
            };
          });
        });
      });

      $scope.publishTemplate = function() {
        var numErrors = 0;
        $scope.variables.forEach(function(section) {
          section.forEach(function(variable) {
            if (variable.type === '' || variable.type === null) {
              numErrors += 1;
              variable.error = true;
            } else {
              variable.error = false;
            }

          });
        });

        if (numErrors > 0) {
          return;
        }

        if (numErrors === 0) {
          $scope.variables = $scope.variables.map(function(section) {
              return section.map(function(variable) {
                return {
                  variable: variable.variable,
                  type: variable.type.type,
                };
              });
            })
          builderSubmit.publishTemplate($scope.variables, $scope.templateId).then(function(data) {
            builderLocationHandler.redirect('/generate')
          });
        }
      }
  }]);
})();
