$(function() {
  // handle accordion glyphicon swapping
  $('#accordion').on('hide.bs.collapse', function(e) {
    // if we are collapsing the currently opened one, flip the arrow
    if (e.target.id === $('#accordion .in').attr('id')) {
      $(e.target).parent().find('.js-glyphicon').
        attr('class', 'glyphicon glyphicon-chevron-down js-glyphicon');
    }
  });

  $('#accordion').on('show.bs.collapse', function(e) {
    // flip the up arrows to down arrows
    $('#accordion').find('.glyphicon-chevron-up').
      attr('class', 'glyphicon glyphicon-chevron-down js-glyphicon');
    // flip the clicked arrow to up
    $(e.target).parent().find('.js-glyphicon').
      attr('class', 'glyphicon glyphicon-chevron-up js-glyphicon');
    // hide the currently opened section
    $('#accordion .in').collapse('hide');
  });

  // turn off all alerts after 3.5 seconds if they aren't closed already
  window.setTimeout(function() {
    $('.flashed-alert').alert('close')
  }, 3500);

  $('#templatePreviewContent').sortable({
    handle: '.js-sortable-handle',
  });

});
