(function() {
  'use strict';

  describe('Services', function() {

    var expect = chai.expect;

    beforeEach(module('builder'));

    var message = 'foo';

    var messageBus;
    beforeEach(inject(function(_messageBus_) {
      messageBus = _messageBus_;
    }))

    describe('messageBus', function() {

      it('should push and pop the message into the messageQueue successfully', function() {
        messageBus.push(message);
        expect(messageBus.pop()).to.include(message);
      });

      it('should return null if there is nothing to pop', function() {
        expect(messageBus.pop()).to.be.null;
      });

      it('should properly reset', function() {
        messageBus.push(message);
        messageBus.reset();
        expect(messageBus.pop()).to.be.null;
      });

      it('should properly return all items from a list', function() {
        messageBus.push(message);
        messageBus.push(message);
        expect(messageBus.list().length).to.equal(2);
      });

    });
  });
}());
