(function() {
  /*

  */
  'use strict';

  builder.service('builderGetData', ['$q', '$http',
    function($q, $http) {
      this.getData = function(url) {
        var deferred = $q.defer();
        $http.get(url).success(function(data) {
          deferred.resolve(data);
        }).error(function(data) {
          console.log(data);
          deferred.reject(data);
        })
        return deferred.promise;
      }
    }
  ]);
})();