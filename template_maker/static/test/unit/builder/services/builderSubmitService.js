(function() {
  'use strict';

  describe('Services', function() {

    var expect = chai.expect;

    beforeEach(module('builder'));

    describe('builderSubmit', function() {
      var builderSubmit, $httpBackend,
        endpoint = '/build/new/save';

      beforeEach(inject(function(_builderSubmit_, _$httpBackend_) {
        builderSubmit = _builderSubmit_;
        $httpBackend = _$httpBackend_;

        var promise = builderSubmit.saveDraft([], true);

        expect(promise).to.have.property('then');
        expect(promise).to.have.property('catch');
        expect(promise).to.have.property('finally');

      }));

      afterEach(function() {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
      });

      it('should successfully resolve if process is true', function() {
        $httpBackend.expectPOST(endpoint).respond(201, 4);
        $httpBackend.flush();
      });

      it('should successfully resolve if process is true', function() {
        $httpBackend.expectPOST(endpoint).respond(400, 'error!');
        $httpBackend.flush();
      })

    });
  });
})();