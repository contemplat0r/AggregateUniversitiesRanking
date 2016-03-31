'use strict';

/* Directives */

app.directive('dropdown', function() {
  return {
    restrict: 'E',
    require: '^ngModel',
    scope: {
      ngModel: '=', // selection
      items: '=',   // items to select from
      callback: '&' // callback
    },
    link: function(scope, element, attrs) {
      element.on('click', function(event) {
        event.preventDefault();
      });

      scope.default = 'Please select item';
      scope.isButton = 'isButton' in attrs;

      // selection changed handler
      scope.select = function(item) {
        scope.ngModel = item;
        if (scope.callback) {
          scope.callback({ item: item });
        }
      };
    },
    templateUrl: 'static/partials/dropdown-template.html'
  };
});
