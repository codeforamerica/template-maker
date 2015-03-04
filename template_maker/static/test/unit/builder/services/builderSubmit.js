(function() {
  'use strict';

  describe('Services', function() {

    var expect = chai.expect;

    beforeEach(module('builder'));

    describe('builderSubmit', function() {
      var builderSubmit, $httpBackend,
        endpoint = '/build/edit/1';

      beforeEach(inject(function(_builderSubmit_, _$httpBackend_) {
        builderSubmit = _builderSubmit_;
        $httpBackend = _$httpBackend_;
      }));

      afterEach(function() {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
      });

      describe('#saveDraft', function() {
        beforeEach(function() {
          var promise = builderSubmit.saveDraft([], 1);

          expect(promise).to.have.property('then');
          expect(promise).to.have.property('catch');
          expect(promise).to.have.property('finally');
        });

        it('should successfully resolve if process is true', function() {
          $httpBackend.expectPUT(endpoint).respond(200, 1);
          $httpBackend.flush();
        });

        it('should reject properly', function() {
          $httpBackend.expectPUT(endpoint).respond(400, 'error!');
          $httpBackend.flush();
        });
      });

      describe('#deleteTemplate', function() {
        beforeEach(function() {
          var promise = builderSubmit.deleteTemplate(1);

          expect(promise).to.have.property('then');
          expect(promise).to.have.property('catch');
          expect(promise).to.have.property('finally');
        });

        it('should successfully delete', function() {
          $httpBackend.expectDELETE(endpoint).respond(201, 4);
          $httpBackend.flush();
        });

        it('should reject', function() {
          $httpBackend.expectDELETE(endpoint).respond(400, 'error!');
          $httpBackend.flush();
        });   
      })
    });
  });
})();