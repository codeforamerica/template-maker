$(function() {

  var variableId = 1;

  function createVariableHtml(modal) {
    var _type = modal.find('.modal-variable-type').val();
    var _name = modal.find('.modal-variable-name').val();

    modal.find('.modal-variable-name').val('');

    return '[[' + _type + ':' + _name + ']]';
  }

  function createVariableShell(modal) {
    var shell = '<span contenteditable=false class="fr-variable"' +
    'id="variable-' + variableId + '">' + '[[]]</span>';
    console.log(shell);
    return shell;
  }

  function insertVariable() {
    // open the modal
    $('#myModal').modal('show');
  }

  // insert the shell on shown
  $('#myModal').on('shown.bs.modal', function(e) {

  });

  // insert the actual variable on save
  $('#myModal').find('.modal-add-variable').on('click', function(e) {
    var modal = $('#myModal');
    $('#variable-' + variableId).html(createVariableHtml(modal));
    variableId++;
  });

  // remove the shell on close
  $('#myModal').on('hide.bs.modal', function(e) {
    $('#variable-' + variableId).remove();
  });


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

            var shell = createVariableShell()
            froala.insertHTML(shell);

            $('#myModal').modal('show');
            $('#myModal').on('hide.bs.modal', function(e) {
              var modal = $(this);

              froala.insertHTML('[[' + modal.find('.modal-variable-type').val() + ':' +
                modal.find('.modal-variable-name').val() + ']]');

            });

          }
        }
      }
    });
});