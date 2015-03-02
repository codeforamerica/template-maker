(function() {
  /*
   The formatHtml service handles all of the logic around highlighting
   variables, appending titles, and generally building and formatting
   HTML elements from structured text.
   */

  builder.service('formatHtml', function() {
    return {
      /*
        highlightVariables takes in contentText, finds all
        text contained between the template symbol ({{ }}), generates
        an array of distinct items, formats them to include a
        <span> for the purpose of highlighting the variables,
        and then replaces the text.
        TOOD: There has to be a better way to do this.
       */      
      highlightVariables: function(contentText) {
        var variableRegex = /({{ |{{).*?(}}| }})/g
        var toHighlight = contentText.match(variableRegex);
        var toHighlightTmp = {},
          highlightedTmp = {},
          highlightedFinal = [],
          toHighlightFinal = [];

        if (toHighlight === null) { return contentText; }

        toHighlight.forEach(function(text) {
          toHighlightTmp[text] = '';
          highlightedTmp['<span class="js-processing-highighted">' + text + "</span>"] = '';
        });

        for (var item in toHighlightTmp) {
          toHighlightFinal.push(item);
        }

        for (var item in highlightedTmp) {
          highlightedFinal.push(item);
        }

        for (var i=0; i<highlightedFinal.length; i++) {
          var find = toHighlightFinal[i];
          var re = new RegExp(find, 'g');
          contentText = contentText.replace(re, highlightedFinal[i]);
        }

        contentText = contentText.replace(/(\\n|\n)/g, '<br/>')

        return contentText;
      },

      /*
        generateSectionHtml takes a section context,
        applies the highlighting from the above method,
        and surrouds the elem with the appropriate tag
       */
      generateSectionHtml: function(section) {
        var elem, _class;
        if (section.type === 'title') { elem = 'h2', _class = 'js-content-title'; }
        else if (section.type === 'section') { elem = 'p', _class = 'js-content-section'; }

        return '<' + elem + ' class="' + _class + '">' +
          this.highlightVariables(section.content) +
          '</' + elem + '>';
      }
    }

  });
})();