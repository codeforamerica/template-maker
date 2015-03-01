(function() {
  /*
    The message bus is a service that allows controllers
    to communicate with each other. It provides four methods:
    push, which adds a message into the queue, list, which
    returns all messages, pop, which returns the latest message,
    and reset, which resets the queue
   */
  'use strict';

  builder.factory('messageBus', function() {
    var messages = [];

    return {
      push: function(obj) {
        messages.push(obj);
      },
      list: function() {
        return messages;
      },
      pop: function() {
        return messages.length ? messages.pop() : null;
      },
      reset: function() {
        messages = [];
      }
    }
  });
})();
