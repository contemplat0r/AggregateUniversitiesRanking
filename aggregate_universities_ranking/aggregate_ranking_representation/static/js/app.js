'use strict';

/* App Module */

var rankingApp = angular.module('rankingApp', [
  //'ngRoute',
  'ui.router',
  //'rankingAnimations',
  'rankingControllers',
  //'rankingFilters',
  //'rankingServices'
]);

//rankingApp.config(['$routeProvider',
rankingApp.config(['$stateProvider', '$urlRouterProvider',
  //function($routeProvider) {
  function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
    $stateProvider.
      //when('/list', {
      state('index', {
        //templateUrl: 'partials/list.html',
        //templateUrl: 'ranktable.html',
        url: '/',
      }).
      state('ranktable', {
        //templateUrl: 'partials/list.html',
        url: '/ranktable',
        templateUrl: 'static/partials/ranktable.html',
        controller: 'RankingListCtrl'
      });
  }]);
