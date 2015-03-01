(function() {
  'use strict';

  describe('Controllers', function() {

    var expect = chai.expect;

    // inject the builder module
    beforeEach(module('builder'));

    describe('processBuilderCtrl', function() {

      var $q, $scope, $rootScope, $controller, $location, messageBus, stub, createController, deferred;
      beforeEach(inject(function(_$q_, _$rootScope_, _$controller_, _$location_, builderGetData) {
        $q = _$q_;
        $rootScope = _$rootScope_.$new()
        $scope = $rootScope.$new();
        $location = _$location_;
        deferred = $q.defer();

        messageBus = { pop: sinon.stub().returns(null) };
        stub = sinon.stub(builderGetData, 'getData').returns(deferred.promise);

        createController = function() {
          return _$controller_('processBuilderCtrl', {
            $scope: $scope,
            messageBus: messageBus,
            builderGetData: builderGetData
          });
        }

      }));

      afterEach(function() {
        stub.restore();
      });

      it('should try to pop the templateId from the messageBus', function() {
        createController();
        expect(messageBus.pop.calledOnce).to.be.true;
      });

      it('should try to get the templateId out of the url', function() {
        var templateId = '1';
        // set the location
        $location.path('/build/edit/' + templateId + '/process')
        // create the controller
        createController();
        // it has the proper id
        expect($scope.templateId).to.equal(templateId);
      });

      it('should properly call the builderGetData service', function() {
        createController();
        expect(stub.callCount).to.equal(1);
      });

      it('should properly set $scope.content and $scope.variables', function() {
        // create the controller
        createController();
        // resolve the promise from the stub (see beforeEach)
        deferred.resolve({template: [{'variables': [1,2,3]}]});
        // run the digest cycle, triggering the controller's processing
        $scope.$digest();
        // do our assertions
        expect($scope.content.length).to.equal(1);
        expect($scope.variables.length).to.equal(1);
        expect($scope.variables[0].length).to.equal(3);
      })

    });
  });
})();