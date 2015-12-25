'use strict';

/* Controllers */

var phonecatControllers = angular.module('aggregaterankingControllers', []);
aggregaterankingControllers.controller('RankingListCtrl', function($scope, $http) {
    $http.get('list').success(function(data) {
        $scope.list = data;
    });
});

/*phonecatControllers.controller('RankingListCtrl', ['$scope', 'Phone',
  function($scope, Phone) {
    $scope.phones = Phone.query();
    $scope.orderProp = 'age';
  }]);

phonecatControllers.controller('PhoneDetailCtrl', ['$scope', '$routeParams', 'Phone',
  function($scope, $routeParams, Phone) {
    $scope.phone = Phone.get({phoneId: $routeParams.phoneId}, function(phone) {
      $scope.mainImageUrl = phone.images[0];
    });

    $scope.setImage = function(imageUrl) {
      $scope.mainImageUrl = imageUrl;
    };
  }]);*/
