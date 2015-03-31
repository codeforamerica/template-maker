$(function() {

  // on initialization, focus the editor and restyle the "add-placeholder" button
  $("#widget").on('editable.initialized', function(e, editor) {
    $('.froala-editor').find('.fr-bttn[data-name="insertPlaceholder"]').css({
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
        'insertPlaceholder', 'sep',
        'bold', 'italic', 'underline', 'sep',
        'formatBlock', 'insertOrderedList','insertUnorderedList', 'insertHorizontalRule', 'sep',
        'undo', 'redo', 'sep',
      ],
      customButtons: {
        insertPlaceholder: {
          title: 'Insert Placeholder',
          icon: {
            type: 'txt',
            value: 'Add Placeholder',
          },
          callback: function () {
            var froala = this;
            insertPlaceholder()

            if (froala.getHTML() === '') {
              // we have to add a non-breaking space character if there is
              // absolutely no html due to some weirdness
              froala.insertHTML('&nbsp' + createPlaceholderShell() + '&nbsp');
            } else {
              froala.insertHTML(createPlaceholderShell() + '&nbsp');
            }

          }
        }
      },

    });

  $('#widget').editable('focus');
  $('#widget').on('editable.contentChanged', function (e, editor) {
    $('#widget').parents('form').trigger('checkform.areYouSure');
  });

  // get the minimum placeholder id which should one more than the total number
  // of placeholders on the page right now
  var placeholderId = Math.max(0, Math.max.apply(null, $.map(
    $('.template-preview-content').find('.js-fr-placeholder'),
    function(d) {
      return +d.id.split('-')[2];
    }))) + 1;

  var placeholders = $.map($('.js-existing-placeholder'), function(d) { return d.innerHTML} );

  function createPlaceholderHtml(modal) {
    var _type = modal.find('.modal-placeholder-type').val();
    var _name = modal.find('.modal-placeholder-name').val();
    var _existing = modal.find('.modal-existing-placeholder');

    // if we don't have a new name or an existing selection, return false
    if (_name === '' && _existing === '-----' ) { return false; }

    // if we have a name defer to that
    if (_name !== '') {
      modal.find('.modal-placeholder-name').val('');
      modal.find('.modal-placeholder-type').val('Text');

      var newPlaceholder = '[[' + _type + '||' + _name + ']]';

      _existing.append($("<option/>", { text: '[[' + _type + '||' + _name + ']]' }));

      return '[[' + _type + '||' + _name + ']]';      
    }
    // otherwise, we must have an existing variable, so return that
    return _existing.val();
  }

  function createPlaceholderId(placeholderId, isElem) {
    // returns a hash if there is an elem, no hash if there isn't
    var placeholderIdRoot = 'template-placeholder-' + placeholderId;
    return isElem ? '#' + placeholderIdRoot : placeholderIdRoot;
  }

  function createPlaceholderShell(modal) {
    // create a shell to insert the placeholder into
    var shell = '<span contenteditable=false class="js-fr-placeholder" data-fr-verified="true" ' +
    'id="' + createPlaceholderId(placeholderId, false) + '"> </span>';
    return shell;
  }

  function insertPlaceholder() {
    // open the modal
    $('#placeholderModal').modal('show');
  }

  // insert the actual placeholder on save
  $('#placeholderModal').find('.modal-add-placeholder').on('click', function(e) {
    var modal = $('#placeholderModal');
    // figure out if we are inserting a new placeholder or modifying an old one
    var curPlaceholder = $('.modal-placeholder-name').attr('data-placeholder-cur-id') ?
      $('.modal-placeholder-name').attr('data-placeholder-cur-id').split('-')[2] :
      placeholderId;
    // update the html
    var newHtml = createPlaceholderHtml(modal);
    if (newHtml) {
      $(createPlaceholderId(curPlaceholder, true)).html(newHtml);
      $('#widget').parents('form').trigger('checkform.areYouSure');
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
    // only increment if we are inserting a new placeholder
    if (typeof(curPlaceholder) === 'number') placeholderId++;
    // reset the name value to be an empty string
    $('.modal-placeholder-name').attr('data-placeholder-cur-id', null);
  });

  $('#placeholderModal').find('.close-bs-modal-no-save').on('click', function(e) {
    // if we are hiding the modal, we need to remove the new shell that we made
    // and reset the values
    $(createPlaceholderId(placeholderId, true)).remove();
    $('.modal-placeholder-name').attr('data-placeholder-cur-id', null);
    $('.modal-placeholder-name').val('');
    $('.modal-placeholder-type').val('Text');
  });

  $('.froala-view').on('dblclick', '.js-fr-placeholder', function(e) {
    editPlaceholder(e.target);
  });

  function editPlaceholder(target) {
    var modalNameInput = $('.modal-placeholder-name');
    var modalTypeInput = $('.modal-placeholder-type');
    // if we are editing an existing placeholder, attach the existing values
    // to the modal field, and the placeholder id as a data attribute so that we
    // can access it later
    modalNameInput.val($(target).html().split('||')[1].slice(0, -2));
    modalTypeInput.val($(target).html().split('||')[0].slice(2, $(target).html().split('||')[0].length));
    modalNameInput.attr('data-placeholder-cur-id', target.id)
    $('#placeholderModal').modal('show');
  }

  var clicking = false, _el;

  // if we click on a placeholder, we have an element and we are clicking
  $('.froala-view').on('mousedown.froalaCustom.movePlaceholder', '.js-fr-placeholder', function(e){
    _el = e.target;
    clicking = true;
  });

  // we need to attach listeners both on the froala editor and the document
  // to get all possible mouseups. when we do, we are no longer clicking
  $('.froala-view').on('mouseup.froalaCustom.movePlaceholder', function(e) {
    clicking = false;
  });

  $('.froala-editor').on('mouseup.froalaCustom.movePlaceholder', function(e) {
    clicking = false;
  });

  $(document).on('mouseup.froalaCustom.movePlaceholder', function(e) {
    clicking = false;
  });

  $('.froala-view').on('mousemove.froalaCustom.movePlaceholder', function(e){
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
