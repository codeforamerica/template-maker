(function() {
  'use strict';

  describe('Controllers', function() {

    var expect = chai.expect;

    // inject the builder module
    beforeEach(module('builder'));

    describe('processBuilderCtrl', function() {

      var $q, $scope, $rootScope, $controller, $location, messageBus, stub, submitStub, redirStub, createController, deferred;
      beforeEach(inject(function(_$q_, _$rootScope_, _$controller_, _$location_, builderGetData, builderSubmit, builderLocationHandler) {
        $q = _$q_;
        $rootScope = _$rootScope_.$new()
        $scope = $rootScope.$new();
        $location = _$location_;
        deferred = $q.defer();

        messageBus = { pop: sinon.stub().returns(null) };
        stub = sinon.stub(builderGetData, 'getData').returns(deferred.promise);
        submitStub = sinon.stub(builderSubmit, 'publishTemplate').returns(deferred.promise);
        redirStub = sinon.stub(builderLocationHandler, 'redirect').returns(deferred.promise);

        createController = function() {
          return _$controller_('processBuilderCtrl', {
            $scope: $scope,
            messageBus: messageBus,
            builderGetData: builderGetData,
            builderSubmit: builderSubmit,
            builderLocationHandler: builderLocationHandler
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
      });

      describe('#publishTemplate', function() {
        beforeEach(function() {
          createController();
          deferred.resolve({template: [{'variables': [1,2,3]}]});
          $scope.$digest();
        });

        it('should set the error property and return properly', function() {
          $scope.publishTemplate();
          $scope.variables[0].forEach(function(variable) {
            expect(variable.error).to.be.true;
          });

          expect(submitStub.callCount).to.equal(0);
        });

        it('should call publishTemplate if we have data types for the variables', function() {
          var formattedVariables = [
            {variable: 1, type: 'unicode'}, {variable: 2, type: 'unicode'}, {variable: 3, type: 'unicode'}
          ];

          $scope.variables[0].forEach(function(variable) {
            variable.type = { type: 'unicode' }
          });

          $scope.publishTemplate();

          assert.equal($scope.variables[0].length, formattedVariables.length);
          assert.equal($scope.variables[0][0].variable, formattedVariables[0].variable);
          assert.equal($scope.variables[0][1].variable, formattedVariables[1].variable);
          assert.equal($scope.variables[0][2].variable, formattedVariables[2].variable);

          expect(submitStub.callCount).to.equal(1);

          deferred.resolve();
          $scope.$digest();
          expect(redirStub.callCount).to.equal(1);
        });

      });

    });
  });
})();