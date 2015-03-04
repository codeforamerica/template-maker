(function() {
  /*
   The builderTextCtrl is the controller that that wraps
   the directives that make up the text editing parts
   of creating a new template (see builderControlsDirective
   and builderContentDirective)
   */
  'use strict';

  builder.controller('builderTextCtrl',['$scope', '$window',
    function($scope, $window) {

      $scope.$on('saveTemplate', function(event, contents) {
        alert('saved!');
      });

    }
  ])
})();