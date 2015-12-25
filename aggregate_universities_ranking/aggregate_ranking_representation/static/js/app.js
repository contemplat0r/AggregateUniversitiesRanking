'use strict';

/* App Module */

var rankingApp = angular.module('rankingApp', [
  'ngRoute',
  //'rankingAnimations',
  'rankingControllers',
  //'rankingFilters',
  //'rankingServices'
]);

rankingApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/list', {
        templateUrl: 'partials/list.html',
        controller: 'RankingListCtrl'
      }).
      //when('/phones/:phoneId', {
      //  templateUrl: 'partials/phone-detail.html',
      //  controller: 'PhoneDetailCtrl'
      //}).
      otherwise({
        redirectTo: '/list'
      });
  }]);
