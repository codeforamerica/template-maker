(function() {
  /*
   The locationHandler is simply a wrapper around different $window
   functions. This abstraction layer allows for much easier and more
   comprehensive testing.
   */
  'use strict';

  builder.factory('builderLocationHandler', ['$window', function($window) {
    return {
      redirect: function(url) {
        $window.location.href = url;
      },
    }
  }]);
})();
