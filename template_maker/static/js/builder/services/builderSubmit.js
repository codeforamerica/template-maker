(function() {
  /*
    The builderSubmit service handles basic $http submissions
    the flask backend. It properly resolves data back when
    promises are resolved.
  */
  'use strict';

  builder.service('builderSubmit', ['$q', '$http',
    function($q, $http) {
      this.saveDraft = function(sections, templateId) {
        // Initialize a new $q promise object
        var deferred = $q.defer();

        // Submit our http request. When it finishes processing
        // the success or error methods will be called, directing the
        // app to do the proper thing
        if (templateId) {
          $http.put('/build/edit/' + templateId, sections).
            success(function(data, status, headers) {
              deferred.resolve(data.template_id)
            }).error(function(data, status, headers) {
              deferred.reject(console.log('failure! ', data));
            });
        } else {
          $http.post('/build/new/save', sections).
            success(function(data, status, headers) {
              deferred.resolve(data.template_id)
            }).error(function(data, status, headers) {
              deferred.reject(console.log('failure! ', data));
            });
        }

        // return the promise object
        return deferred.promise;
      };

      this.deleteTemplate = function(templateId) {
        var deferred = $q.defer();

        $http.delete('/build/edit/' + templateId).
          success(function() {
            deferred.resolve(templateId);
          }).error(function() {
            deferred.reject(templateId);
          });

        return deferred.promise;
      };

      this.publishTemplate = function(sections, templateId) {
        var deferred = $q.defer();

        $http.post('/build/edit/' + templateId + '/publish', sections).
          success(function(data, status, headers) {
            deferred.resolve(data);
          }).error(function(data, status, headers) {
            deferred.reject(data);
          });

        return deferred.promise;
      }
    }
  ]);
})();
