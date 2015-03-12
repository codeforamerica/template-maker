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

  // remove the shell on close
  $('#myModal').on('hide.bs.modal', function(e) {
    $(createVariableId(variableId, true)).remove();
  });


});