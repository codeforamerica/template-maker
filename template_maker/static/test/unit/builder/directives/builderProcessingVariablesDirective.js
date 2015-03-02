(function() {
  'use strict';

  describe('Directives', function() {

    var expect = chai.expect;

    beforeEach(module('builder'));

    describe('builderProcessingVariablesDirective', function() {
      var $httpBackend, $scope, $compile, el;

      beforeEach(inject(function(_$rootScope_, _$compile_, _$httpBackend_) {
        $scope = _$rootScope_.$new();
        $compile = _$compile_;
        $httpBackend = _$httpBackend_;

        // seed content
        $scope.variables = [[{variable: 'foo'}], [{content: 'bar'}, {variable: 'baz'}]];

        // create a new builder-content angular element
        el = angular.element('<template-variables variables="variables"></template-variables>');
        $compile(el)($scope);
        // expect there to be no children
        expect(el.children()).to.have.length(0);
        // make a mock request and return a simple mocked-up template
        $httpBackend.expectGET('../../../static/js/builder/partials/processing-variables.html').
          respond(200, '' +
            '<div ng-repeat="section in variables">' +
              '<div id="variable" ng-repeat="variable in section">{[variable.variable]}</div><hr/>' +
            '</div>');
        $httpBackend.flush();
      }));

      afterEach(function() {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
      });

      it('should append elements properly', function() {
        // there should be two sections
        expect(el.children()).to.have.length(2);
        // there should be three variables
        // TODO: Figure out how to do this
      });
    });

  });

})();