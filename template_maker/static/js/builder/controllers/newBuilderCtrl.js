(function() {
  'use strict';

  builder.controller('newBuilderCtrl',['$scope', 
    function($scope) {
      $scope.$on('saveTemplate', function(event, contents) {
        alert('saved!')
      })
    }
  ])
})();