(function() {
  'use strict';

  describe('Services', function() {

    var expect = chai.expect;

    beforeEach(module('builder'));

    describe('builderGetDataService', function() {
      var builderGetData, $httpBackend,
        mockTemplate = [
          {
            content: 'foo',
            type: 'title',
            variables: []
          }
        ];

      beforeEach(inject(function(_builderGetData_, _$httpBackend_) {
        builderGetData = _builderGetData_;
        $httpBackend = _$httpBackend_;

        var promise = builderGetData.getData('/foo');
        // ensure that the return value is a promise that has the correct properties
        expect(promise).to.have.property('then');
        expect(promise).to.have.property('catch');
        expect(promise).to.have.property('finally');

      }));

      afterEach(function() {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
      });

      it('should successfully resolve the promise at the correct endpoint if appropriate', function() {
        $httpBackend.expectGET('/foo').respond(200);
        $httpBackend.flush();
      });

      it('should successfully reject the promise at the correct endpoint if appropriate', function() {
        $httpBackend.expectGET('/foo').respond(400);
        $httpBackend.flush();
      });
    })
  })

})();