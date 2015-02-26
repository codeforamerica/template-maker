(function() {
  /*

  */
  'use strict';

  builder.controller('processBuilderCtrl', ['$scope', '$location', 'builderGetData', 'messageBus',
    function($scope, $location, builderGetData, messageBus) {
      // try to get the id from the messages
      // otherwise get it from the url
      var templateId = messageBus.pop();
      if (templateId === null) {
        var urlParts = $location.absUrl().split('/');
        templateId = urlParts[urlParts.length - 2];
      }
      builderGetData.getData('/build/edit/' + templateId + '/process').then(function(data) {
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
