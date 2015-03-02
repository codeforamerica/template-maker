(function() {
  'use strict';

  describe('Directives', function() {

    var expect = chai.expect;

    beforeEach(module('builder'));

    describe('builderControlsDirective', function() {
      var $q, $httpBackend, $scope, $compile, $window, builderSubmit, el, deferred;

      beforeEach(inject(function(_$q_, _$httpBackend_, _$rootScope_, _$compile_, _$window_, _builderSubmit_) {
        $q = _$q_;
        $scope = _$rootScope_;
        $httpBackend = _$httpBackend_;
        $compile = _$compile_;
        $window = {location: {href: 0}};

        deferred = $q.defer()
        // submitStub = sinon.stub(builderSubmit, 'saveDraft').returns(deferred.promise);
        builderSubmit = _builderSubmit_

        el = angular.element('<builder-controls></builder-controls');
        $compile(el)($scope);

        $httpBackend.expectGET('../static/js/builder/partials/builder-controls.html').
          respond(200, '<div></div>');
        $httpBackend.flush();
        // expect it to always initialize with the title and section
        expect($scope.sections).to.have.length(2);
        // reset $scope.sections
        $scope.sections = [];
      }));

      afterEach(function() {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
      });

      it('should add "title" section on click of addTitle()', function() {
        expect($scope.sections).to.have.length(0);
        $scope.addTitle();
        expect($scope.sections).to.have.length(1);
        expect($scope.sections[0]['type']).to.equal('title');
      });

      it('should add a "section" section on click of addSection()', function() {
        expect($scope.sections).to.have.length(0);
        $scope.addSection();
        expect($scope.sections).to.have.length(1);
        expect($scope.sections[0]['type']).to.equal('section');
      });

      it('should emit the saveTemplate signal on template save', function() {
        $scope.$emit = sinon.spy();
        $scope.saveTemplate();
        expect($scope.$emit.callCount).to.equal(1);
        var args = $scope.$emit.firstCall.args;
        expect(args).to.contain('saveTemplate');
        expect(args).to.contain($scope.sections);
      });

      describe('#processTemplate', function() {
        beforeEach(function() {
          // seed the sections with all permutations of acceptable variables
          $scope.sections = [{content: '{{ foo}} {{ bar }} {{baz }} {{qux}}'}];
          $scope.processTemplate();
        });

        it('should properly pick up all possible permutations as variables', function() {
          expect($scope.sections[0]['variables']).to.have.length(4);
          $httpBackend.expectPOST('/build/new/save').respond(400);
          $httpBackend.flush()
        });

        it.skip('should call the builderSubmit service to submit the job', function() {
          // TODO: Look up proper procedure for testing $window
          $httpBackend.expectPOST('/build/new/save').respond(200, {template_id: 1});
          $httpBackend.flush();
        });
      });

      it.skip('should add and remove classes based on scroll position', function() {
        // TODO: Look up the proper way to simulate a scroll event on $window

      });

    });
  });
})();