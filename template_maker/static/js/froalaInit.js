$(function() {

  function getSelectionText() {
    var text = '';
    if (window.getSelection) {
      text = window.getSelection().toString();
    } else if (document.selection && document.selection.type != "Control") {
      text = document.selection.createRange().text;
    }
    return text;
  }

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

            $('#myModal').modal('show');
            $('#myModal').on('hide.bs.modal', function(e) {
              var modal = $(this);
              froala.insertHTML('[[' + modal.find('.modal-variable-type').val() + ':' +
                modal.find('.modal-variable-name').val() + ']]');

              froala.sync()
            });
          }
        }
      }
    })
});