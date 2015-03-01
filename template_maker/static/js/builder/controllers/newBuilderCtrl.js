(function() {
  /*
    The builder controller encompasses the directives that make up
    each template builder.
  */
  'use strict';

  builder.controller('newBuilderCtrl',['$scope', '$window',
    function($scope, $window) {

      $scope.$on('saveTemplate', function(event, contents) {
        alert('saved!');
      });

    }
  ])
})();