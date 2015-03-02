(function() {
  'use strict';

  describe('Directives', function() {

    var expect = chai.expect;

    beforeEach(module('builder'));

    describe('builderOptionsDirective', function() {
      var $httpBackend, $scope, $compile, el;

      beforeEach(inject(function(_$httpBackend_, _$rootScope_, _$compile_) {
        $httpBackend = _$httpBackend_;
        $scope = _$rootScope_.$new();
        $compile = _$compile_;

        el = angular.element('<textarea builder-options setfocus="true"></textarea>');
        el[0].focus = sinon.spy();
        $compile(el)($scope);
      }));

      it('should call focus on the element', function() {
        expect(el[0].focus.callCount).to.equal(1);
      });
    });

  });

})();