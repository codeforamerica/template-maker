(function() {
  /*

  */
  'use strict';

  builder.controller('processBuilderCtrl', ['$scope', 'builderGetData',
    function($scope, builderGetData) {

      builderGetData.getData('/build/edit/1/process').then(function(data) {
        $scope.content = data.template;
        // extract and flatten the variable names from each section
        $scope.variables = data.template.map(function(datum) {
          return datum.variables.map(function(variable) {
            return {
              variable: variable,
              type: ''
            };
          });
        });
      });

    }
  ]);
})();
