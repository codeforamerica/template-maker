(function() {
  'use strict';

  describe('Controllers', function() {

    var expect = chai.expect;

    // inject the builder module
    beforeEach(module('builder'));

    describe('templateListCtrl', function() {
      var $q, $scope, $rootScope, windowMock, $controller, deferred, builderSubmit, stub, elStub;
      beforeEach(inject(function(_$q_, _$rootScope_, _$controller_, builderSubmit) {
        $q = _$q_;
        $rootScope = _$rootScope_.$new();
        $scope = $rootScope.$new();
        windowMock = { confirm: function(msg) { return true; }};

        deferred = $q.defer();

        stub = sinon.stub(builderSubmit, 'deleteTemplate').returns(deferred.promise);
        elStub = sinon.stub(angular, 'element').returns({ remove: sinon.spy() });

        var controller = _$controller_('templateListCtrl', {
          $scope: $scope,
          $window: windowMock,
          builderSubmit: builderSubmit
        });

        $scope.deleteTemplate(1);
      }));

      afterEach(function() {
        stub.restore();
        elStub.restore();
      });

      it('should call the deleteTemplate method', function() {
        expect(stub).to.be.called;
      });

      it('should call a remove to delete the element', function() {
        deferred.resolve(1);
        $scope.$digest();
        expect(elStub.remove).to.be.called;
      });

    });
  });
})();