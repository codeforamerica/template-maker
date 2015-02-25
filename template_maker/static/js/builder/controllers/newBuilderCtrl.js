(function() {
  /*
    The builder controller encompasses the directives that make up
    each template builder. The controller handles events that run
    over the entire builder
  */
  'use strict';

  builder.controller('newBuilderCtrl',['$scope',
    function($scope) {

      $scope.$on('saveTemplate', function(event, contents) {
        alert('saved!');
      });

    }
  ])
})();