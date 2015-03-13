$(function() {

  $('#widget')
    .html($('#sectionText').html())
    .editable({
      inlineMode: false,
      height: 450,
      buttons: [
        'bold', 'italic', 'underline', 'formatBlock', 'insertOrderedList',
        'insertUnorderedList', 'insertVariable', 'undo', 'redo',
      ],
      customButtons: {
        insertVariable: {
          title: 'Insert Variable',
          icon: {
            type: 'font',
            value: 'fa fa-plus'
          },
          callback: function () {
            var froala = this;
            insertVariable()

            froala.insertHTML(createVariableShell());
          }
        }
      }
    });

  // get the minimum variable id which should one more than the total number
  // of variables on the page right now
  variableId = $($('#widget').editable('getHTML')).find('.fr-variable').length + 1;

  function createVariableHtml(modal) {
    var _type = modal.find('.modal-variable-type').val();
    var _name = modal.find('.modal-variable-name').val();

    modal.find('.modal-variable-name').val('');

    return '[[' + _type + ':' + _name + ']]';
  }

  function createVariableId(variableId, isElem) {
    // returns a hash if there is an elem, no hash if there isn't
    var variableIdRoot = 'template-variable-' + variableId;
    return isElem ? '#' + variableIdRoot : variableIdRoot;
  }

  function createVariableShell(modal) {
    var shell = '<span contenteditable=false class="fr-variable"' +
    'id="' + createVariableId(variableId, false) + '">' + '[[]]</span>';
    return shell;
  }

  function insertVariable() {
    // open the modal
    $('#myModal').modal('show');
  }

  // insert the actual variable on save
  $('#myModal').find('.modal-add-variable').on('click', function(e) {
    var modal = $('#myModal');
    $(createVariableId(variableId, true)).html(createVariableHtml(modal));
    variableId++;
  });

  $('.fr-variable').on('dblclick', function(e) {
    editVariable(e.target);
  });

  // remove the shell on close
  $('#myModal').on('hide.bs.modal', function(e) {
    $(createVariableId(variableId, true)).remove();
  });

  function editVariable(target) {
    $('.modal-variable-name').val(
      $(target).html().split(':')[1].slice(0, -2)
    );
    $('#myModal').modal('show');
  }

  var clicking = false, _el;

  $('.fr-variable').on('mousedown.froalaCustom.moveVariable', function(e){
    _el = e.target;
    clicking = true;
  });

  $('.froala-view').on('mouseup.froalaCustom.moveVariable', function(e){
    clicking = false;
  });

  $(document).on('mouseup.froalaCustom.moveVariable', function(e) {
    clicking = false;
  });

  $('fr-variable').on('')

  $('.froala-view').on('mousemove.froalaCustom.moveVariable', function(e){
    e.preventDefault();
    if (clicking === false || !_el) return;

    var range, textRange, x = e.clientX, y = e.clientY;

    //remove the old pin
    _el = _el.parentNode.removeChild(_el);

    // Try the standards-based way first
    if (document.caretPositionFromPoint) {
      var pos = document.caretPositionFromPoint(x, y);
      range = document.createRange();
      range.setStart(pos.offsetNode, pos.offset);
      range.collapse();
    }
    // Next, the WebKit way
    else if (document.caretRangeFromPoint) {
      range = document.caretRangeFromPoint(x, y);
    }
    // Finally, the IE way
    else if (document.body.createTextRange) {
      textRange = document.body.createTextRange();
      textRange.moveToPoint(x, y);
      var spanId = "temp_" + ("" + Math.random()).slice(2);
      textRange.pasteHTML('<span id="' + spanId + '">&nbsp;</span>');
      var span = document.getElementById(spanId);
      //place the new pin
      span.parentNode.replaceChild(_el, span);
    }
    if (range) {
      //place the new pin
      range.insertNode(_el);
    }
  });

});