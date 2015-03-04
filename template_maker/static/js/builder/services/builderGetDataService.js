(function() {
  /*
   The builderGetData service is responsible for basic
   async data fetching: the getData method takes a URL
   and returns a promise, which resolves with whatever
   is returned from the server
   */
  'use strict';

  builder.service('builderGetData', ['$q', '$http',
    function($q, $http) {
      this.getData = function(url) {
        var deferred = $q.defer();
        $http.get(url).success(function(data) {
          deferred.resolve(data);
        }).error(function(data) {
          deferred.reject(data);
        })
        return deferred.promise;
      }
    }
  ]);
})();