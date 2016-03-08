'use strict';

/* App Module */

//var rankingApp = angular.module('rankingApp', ['ngRoute', 'rankingControllers', 'ngAnimate', 'treasure-overlay-spinner', 'ng.bs.dropdown']);
var rankingApp = angular.module('rankingApp', ['ngRoute', 'rankingControllers', 'ngAnimate', 'treasure-overlay-spinner', 'ui.bootstrap', 'ng.bs.dropdown']);

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

rankingApp.run(run);

run.$inject = ['$rootScope'];
function run($rootScope) {
    $rootScope.spinner = {
        active : false,
        on : function() {
            this.active = true;
            console.log('spinner on');
        },
        off : function() {
            this.active = false;
            console.log('spinner off');
        }
    };
}

