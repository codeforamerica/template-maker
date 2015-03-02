(function() {
  'use strict';

  describe('Services', function() {

    var expect = chai.expect;

    beforeEach(module('builder'));

    var formatHtml;
    var hasVariable = '{{ foo }} {{bar }} {{ baz}} {{qux}}';
    var formattedHasVariable = '<span class="js-processing-highighted">{{ foo }}</span> ' +
      '<span class="js-processing-highighted">{{bar }}</span> ' +
      '<span class="js-processing-highighted">{{ baz}}</span> ' +
      '<span class="js-processing-highighted">{{qux}}</span>';
    var noVariable = '{{ } } {{{ }';

    var testTitle = {type: 'title', content: 'foo'};
    var htmlTestTitle = '<h2 class="js-content-title">foo</h2>';

    var testSection = {type: 'section', content: '{{bar}}'};
    var htmlTestSection = '<p class="js-content-section">' +
      '<span class="js-processing-highighted">{{bar}}</span>' +
      '</p>'

    beforeEach(inject(function(_formatHtml_) {
      formatHtml = _formatHtml_;
    }))

    describe('formatHtml', function() {
      describe('#highlightVariables', function() {
        it('should return the value if there are no {{ }} enclosures', function() {
          var formatted = formatHtml.highlightVariables(noVariable);
          expect(formatted).to.equal(noVariable);
        });

        it('should detect and autoupdate all possible {{ }} enclosures', function() {
          var formatted = formatHtml.highlightVariables(hasVariable);
          expect(formatted).to.equal(formattedHasVariable);
        });
      });

      describe('#generateSectionHtml', function() {
        it('should properly format a title', function() {
          var formatted = formatHtml.generateSectionHtml(testTitle);
          expect(formatted).to.equal(htmlTestTitle);
        });

        it('should properly format a section', function() {
          var formatted = formatHtml.generateSectionHtml(testSection);
          expect(formatted).to.equal(htmlTestSection);
        });

      });
    });
  });
}());
