(function() {
  'use strict';

  describe('Controllers', function() {

    var expect = chai.expect;

    // inject the builder module
    beforeEach(module('builder'));

    describe('builderTextCtrl', function() {
      var $scope, $rootScope, $controller, alert;
      beforeEach(inject(function(_$rootScope_, _$controller_) {
        $rootScope = _$rootScope_.$new()
        $scope = $rootScope.$new();

        var controller = _$controller_('builderTextCtrl', {
          $scope: $scope,
          alert: sinon.spy()
        });

      }));

      it('should trigger an alert on save', function() {
        $rootScope.$broadcast('saveTemplate');
        expect(alert).to.be.called;
      })

    });
  });
})();