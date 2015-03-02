(function() {
  /*
    The message bus is a service that allows controllers
    to communicate with each other. It provides four methods:
    push, which adds a message into the queue, list, which
    returns all messages, pop, which returns the latest message,
    and reset, which resets the queue
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
