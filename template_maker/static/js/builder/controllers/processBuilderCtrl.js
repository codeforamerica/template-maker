(function() {
  /*

  */
  'use strict';

  builder.controller('processBuilderCtrl', ['$scope', 'builderGetData',
    function($scope, builderGetData) {

      builderGetData.getData('/build/edit/1/process').then(function(data) {
        $scope.content = data;
      });

    }
  ]);
})();