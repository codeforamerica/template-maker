$(function() {

  // on initialization, focus the editor and restyle the "add-variable" button
  $("#widget").on('editable.initialized', function(e, editor) {
    $('.froala-editor').find('.fr-bttn[data-name="insertVariable"]').css({
      'width': '120px', 'font-size': '14px'
    });
  });

  var mainForm = $('#widget').parents('form');
  mainForm.areYouSure({
    'fieldSelector': ':input:not(input[type=submit])'
  })
  mainForm.find('input').keypress(function(event) {
    if (event.which === 13) {
      event.preventDefault();
    }
  });

  $('#widget')
    .html($('#sectionText').html())
    .editable({
      inlineMode: false,
      height: 450,
      buttons: [
        'insertVariable', 'sep',
        'bold', 'italic', 'underline', 'sep',
        'formatBlock', 'insertOrderedList','insertUnorderedList', 'insertHorizontalRule', 'sep',
        'undo', 'redo', 'sep',
      ],
      customButtons: {
        insertVariable: {
          title: 'Insert Placeholder',
          icon: {
            type: 'txt',
            value: 'Add Placeholder',
          },
          callback: function () {
            var froala = this;
            insertVariable()

            if (froala.getHTML() === '') {
              // we have to add a non-breaking space character if there is
              // absolutely no html due to some weirdness
              froala.insertHTML('&nbsp' + createVariableShell() + '&nbsp ');
            } else {
              froala.insertHTML(createVariableShell() + '&nbsp ');
            }

          }
        }
      },

    });

  $('#widget').editable('focus');
  $('#widget').on('editable.contentChanged', function (e, editor) {
    $('#widget').parents('form').trigger('checkform.areYouSure');
    mainForm.areYouSure({
      'fieldSelector': ':input:not(input[type=submit])'
    });
  });

  // get the minimum variable id which should one more than the total number
  // of variables on the page right now
  variableId = Math.max(0, Math.max.apply(null, $.map(
    $($('#widget').editable('getHTML')).find('.fr-variable'), 
    function(d) {
      return +d.id.split('-')[2];
    })))

  function createVariableHtml(modal) {
    var _type = modal.find('.modal-variable-type').val();
    var _name = modal.find('.modal-variable-name').val();

    if (_name === '') { return false; }

    modal.find('.modal-variable-name').val('');
    modal.find('.modal-variable-type').val('Text');

    return '[[' + _type + '||' + _name + ']]';
  }

  function createVariableId(variableId, isElem) {
    // returns a hash if there is an elem, no hash if there isn't
    var variableIdRoot = 'template-variable-' + variableId;
    return isElem ? '#' + variableIdRoot : variableIdRoot;
  }

  function createVariableShell(modal) {
    // create a shell to insert the variable into
    var shell = '<span contenteditable=false class="fr-variable" data-fr-verified="true" ' +
    'id="' + createVariableId(variableId, false) + '"> </span>';
    return shell;
  }

  function insertVariable() {
    // open the modal
    $('#variableModal').modal('show');
  }

  // insert the actual variable on save
  $('#variableModal').find('.modal-add-variable').on('click', function(e) {
    var modal = $('#variableModal');
    // figure out if we are inserting a new variable or modifying an old one
    var curVariable = $('.modal-variable-name').attr('data-variable-cur-id') ?
      $('.modal-variable-name').attr('data-variable-cur-id').split('-')[2] :
      variableId;
    // update the html
    var newHtml = createVariableHtml(modal);
    if (newHtml) {
      $(createVariableId(curVariable, true)).html(newHtml);
      modal.modal('hide');
    } else {
      var body = modal.find('.modal-body');
      if (body.find('.alert').length === 0) {
        body.prepend('<div class="alert alert-danger alert-dismissable">' +
        '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
        '<span>Placeholders cannot be empty!</span>' +
        '</div>'
        )
      }
      return
    }
    // only increment if we are inserting a new variable
    if (typeof(curVariable) === 'number') variableId++;
    // reset the name value to be an empty string
    $('.modal-variable-name').attr('data-variable-cur-id', null);
  });

  $('#variableModal').find('.close-bs-modal-no-save').on('click', function(e) {
    // if we are hiding the modal, we need to remove the new shell that we made
    // and reset the values
    $(createVariableId(variableId, true)).remove();
    $('.modal-variable-name').attr('data-variable-cur-id', null);
    $('.modal-variable-name').val('');
    $('.modal-variable-type').val('Text');
  });

  $('.froala-view').on('dblclick', '.fr-variable', function(e) {
    editVariable(e.target);
  });

  function editVariable(target) {
    var modalNameInput = $('.modal-variable-name');
    var modalTypeInput = $('.modal-variable-type');
    // if we are editing an existing variable, attach the existing values
    // to the modal field, and the variable id as a data attribute so that we
    // can access it later
    modalNameInput.val($(target).html().split(':')[1].slice(0, -2));
    modalTypeInput.val($(target).html().split(':')[0].slice(2, $(target).html().split(':')[0].length));
    modalNameInput.attr('data-variable-cur-id', target.id)
    $('#variableModal').modal('show');
  }

  var clicking = false, _el;

  // if we click on a variable, we have an element and we are clicking
  $('.froala-view').on('mousedown.froalaCustom.moveVariable', '.fr-variable', function(e){
    _el = e.target;
    clicking = true;
  });

  // we need to attach listeners both on the froala editor and the document
  // to get all possible mouseups. when we do, we are no longer clicking
  $('.froala-view').on('mouseup.froalaCustom.moveVariable', function(e) {
    clicking = false;
  });

  $('.froala-editor').on('mouseup.froalaCustom.moveVariable', function(e) {
    clicking = false;
  });

  $(document).on('mouseup.froalaCustom.moveVariable', function(e) {
    clicking = false;
  });

  $('.froala-view').on('mousemove.froalaCustom.moveVariable', function(e){
    if (clicking === false || !_el) return;
    e.preventDefault();

    var range, textRange, x = e.clientX, y = e.clientY;

    // detach and store the old element outside the DOM
    _el = _el.parentNode.removeChild(_el);

    // Try to set the range the standards-based way first
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
      // place the element at the beginning of the range
      range.insertNode(_el);
    }
  });
});
