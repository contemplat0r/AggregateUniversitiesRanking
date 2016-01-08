'use strict';

/* App Module */

//var rankingApp = angular.module('rankingApp', ['ngRoute']);
var rankingApp = angular.module('rankingApp', ['ngRoute', 'rankingControllers']);

rankingApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/start', {
                templateUrl: 'static/partials/start.html',
                controller: 'Ctrl1'
            }).
            when('/ranktable', {
                templateUrl: 'static/partials/ranktable.html',
                //controller: 'Ctrl2'
                controller: 'RankingTableCtrl'
            }).
            otherwise({
                redirectTo: '/start'
            });
    }]);

rankingApp.controller("Ctrl1", function($scope) {
    $scope.test="This is working test1"
});
rankingApp.controller("Ctrl2", function($scope) {
    $scope.test="This is working test2"
});
