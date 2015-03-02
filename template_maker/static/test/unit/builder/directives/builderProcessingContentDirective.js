(function() {
  'use strict';

  describe('Directives', function() {

    var expect = chai.expect;

    beforeEach(module('builder'));

    describe('builderProcessingContentDirective', function() {
      var $httpBackend, $compile, $timeout, $scope, el;
      beforeEach(inject(function(_$compile_, _$timeout_, _$rootScope_, _$httpBackend_) {
        $compile = _$compile_;
        $timeout = _$timeout_;
        $scope = _$rootScope_.$new();
        $httpBackend = _$httpBackend_;

        $scope.content = [{content: '{{ foo }}', type: 'title'}, {content: 'foo', type: 'section'}];

        el = angular.element('<template-content content="content"></template-content>');
        $compile(el)($scope);
        expect(el.children()).to.have.length(0);
        $httpBackend.expectGET('../../../static/js/builder/partials/processing-content.html').
          respond(200, '' +
            '<div ng-repeat="section in formattedContent">' +
              '{[ section.content ]}' +
            '</div>'
          );
        $httpBackend.flush();
      }));

      afterEach(function() {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
      });

      it('should generate section html for each section and add it to the element', function() {
        $timeout.flush();
        expect(el.children()).to.have.length(2);
      })

    });
  });

})();