(function() {
  /*
    The builderSubmit service handles $http posting to
    the flask backend. It properly resolves data back when
    promises are resolved.
  */
  'use strict';

  builder.service('builderSubmit', ['$q', '$http',
    function($q, $http) {
      this.saveDraft = function(sections, process) {
        // Initialize a new $q promise object
        var deferred = $q.defer();

        // Submit our http request. When it finishes processing
        // the success or error methods will be called, directing the
        // app to do the proper thing
        $http.post('/build/new/save', sections).
          success(function(data, status, headers) {
            if (process === true) {
              deferred.resolve(data.template_id)
            }
          }).error(function(data, status, headers) {
            deferred.resolve(console.log('failure! ', data));
          });

        // return the promise object
        return deferred.promise;
      };
    }
  ]);
})();
