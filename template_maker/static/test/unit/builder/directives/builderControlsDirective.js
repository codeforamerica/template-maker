(function() {
  'use strict';

  describe('Directives', function() {

    var expect = chai.expect;

    beforeEach(module('builder'));

    describe('builderControlsDirective', function() {
      var $httpBackend, $scope, $compile, builderSubmit, messageBus, el, redirStub;

      beforeEach(inject(function(_$httpBackend_, _$rootScope_, _$compile_, _builderSubmit_, _messageBus_, _builderLocationHandler_) {
        $scope = _$rootScope_;
        $httpBackend = _$httpBackend_;
        $compile = _$compile_;

        messageBus = _messageBus_;
        redirStub = sinon.stub(_builderLocationHandler_, 'redirect');
        builderSubmit = _builderSubmit_

        el = angular.element('<builder-controls></builder-controls');
        $compile(el)($scope);

        $httpBackend.expectGET('../static/js/builder/partials/builder-controls.html').
          respond(200, '<div style="height:100px" class="builder-controls"></div>');
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

        it('should call the builderSubmit service to submit the job', function() {
          $httpBackend.expectPOST('/build/new/save').respond(200, {template_id: 1});
          $httpBackend.flush();
          expect(redirStub.callCount).to.equal(1);
          assert(redirStub.calledWith('/build/edit/1/process'));
        });

        it('should push the templateId into the messageBus', function() {
          $httpBackend.expectPOST('/build/new/save').respond(200, {template_id: 2});
          $httpBackend.flush();
          expect(messageBus.pop()).to.equal(2);
        });
      });

      it.skip('should add and remove classes based on scroll position', function() {

      });

    });
  });
})();