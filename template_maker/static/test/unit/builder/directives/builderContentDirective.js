(function() {
  'use strict';

  describe('Directives', function() {

    var expect = chai.expect;

    beforeEach(module('builder'));

    describe('builderContentDirective', function() {
      var $httpBackend, $scope, $compile, el;

      beforeEach(inject(function(_$rootScope_, _$compile_, _$httpBackend_) {
        $scope = _$rootScope_.$new();
        $compile = _$compile_;
        $httpBackend = _$httpBackend_;

        // seed content
        $scope.sections = [{content: 'foo'}, {content: 'bar'}];

        // create a new builder-content angular element
        el = angular.element('<builder-content></builder-content>');
        $compile(el)($scope);
        // expect there to be no children
        expect(el.children()).to.have.length(0);
        // make a mock request and return a simple mocked-up template
        $httpBackend.expectGET('../static/js/builder/partials/builder-content.html').
          respond(200, '<div ng-repeat="section in sections"><p>{[section]}</p></div>');
        $httpBackend.flush();
      }));

      afterEach(function() {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
      });

      it('should append elements properly', function() {
        expect(el.children()).to.have.length(2);
      });

      it('should properly delete elements', function() {
        expect($scope.sections).to.have.length(2);
        $scope.deleteElem(1);
        expect($scope.sections).to.have.length(1);
      });
    });

  });

})();