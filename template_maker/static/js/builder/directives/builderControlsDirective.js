(function() {
  /*
    The controls directive is the set of UI components that
    controls how new sections, titles, and variables are added
    to the page.
  */
  'use strict';

  builder.directive('builderControls', ['$timeout', '$window', 'builderSubmit',
    function($timeout, $window, builderSubmit) {
      function link(scope, elem, attrs) {
        /*
          Initialize our page model. Sections will be an array of all
          of the objects for each title and section that is on the page.
          Each section object contains information about the html element
          that should be used to render it (its elem) and potentially
          more information that should be used (its type). Additionally,
          there is placeholder text and a specific destination for two-way
          data binding via ng-model (the content key)

        */
        scope.sections = [];

        function addTitle() {
          scope.sections.push({
            elem: 'input', type: 'text', _class: 'js-builder-title form-control',
            placeholder: 'Enter a title here', variables: [], content: ''
          })
        };

        function addSection() {
          scope.sections.push({
            elem: 'textarea', type: 'textarea', _class: 'js-builder-section form-control',
            placeholder: 'Enter a bit about your section here', variables: [], content: ''
          });
        };

        // We are going to seed the page with a blank title and a blank
        // section by default
        addTitle();
        addSection();

        // Handle click events from the template to add additional titles
        // and larger sections
        scope.addTitle = function() { addTitle(); };
        scope.addSection = function() { addSection(); };

        scope.saveTemplate = function() { scope.$emit('saveTemplate', scope.sections); };
        scope.processTemplate = function() {
          builderSubmit.saveDraft(scope.sections, true).then(function(templateId) {
            $window.location.href = $window.location.origin +
              '/build/edit/' + templateId + '/process';
          });
        };

        // This hooks onto scroll and locks the builder controls (the UI
        // elements to add an additional button) to the top of the page.
        // TODO: Figure out a better way to do this.
        angular.element($window).bind('scroll', function() {
          var builderControlsElem = angular.element('.builder-controls');
          if (this.pageYOffset >= 20) {
            builderControlsElem.addClass('js-builder-controls-position-fixed');
          } else {
            builderControlsElem.removeClass('js-builder-controls-position-fixed');
          }
        })

      };

      return {
        restrict: 'AE',
        templateUrl: '../static/js/builder/partials/builder-controls.html',
        // This directive is interacting with another directive in the same
        // controller scope, so we set the transclude to true here.
        transclude: true,
        link: link
      };
    }
  ]);

})();