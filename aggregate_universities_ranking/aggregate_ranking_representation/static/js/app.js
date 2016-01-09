'use strict';

/* App Module */

//var rankingApp = angular.module('rankingApp', ['ngRoute']);
var rankingApp = angular.module('rankingApp', ['ngRoute', 'rankingControllers']);

rankingApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/start', {
                templateUrl: 'static/partials/start.html',
                controller: 'StartController'
            }).
            when('/ranktable', {
                templateUrl: 'static/partials/ranktable.html',
                controller: 'RankingTableController'
            }).
            otherwise({
                redirectTo: '/start'
            });
    }]);


