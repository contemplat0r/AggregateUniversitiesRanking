'use strict';

/* Controllers */

var rankingApp = angular.module('rankingApp', []);


rankingApp.controller('RankingListCtrl', function($scope, $http) {
    $scope.name = 'World';
    $scope.rankinglist = [
        {'name' : 'QS'},
        {'name' : 'THE'}
    ];
    $http.get('api/table?format=json').success(function(data) {
        $scope.table = data;
    });
});


rankingApp.controller('RankingCheckController', function($scope, $http) {
    $scope.rankingchecklist  = [
        {name : 'QS', value : false},
        {name : 'THE', value : true},
        {name : 'NTU', value : false}
    ];
    $scope.sendselected = function(rankingchecklist) {
    //$scope.sendselected = function() {
        console.log('Entry in sendselected');
        var selectednames = [];
        console.log('Sendselected: selectednames array declared');
        /*for (var record in rankingchecklist) {
            console.log('Sendselected, record.name: ' + record.name);
        //for (var record in $scope.rankingchecklist) {
            //if (record.value === true) {
            //    selectednames.push(record.name);
            //}
            if (record['value'] == true) {
                console.log('Sendselected, value == true, for name: ' + record['name']);
                selectednames.push(record['name']);
            }
        }*/
        rankingchecklist.forEach(function(item, i, rankingchecklist) {
            if (item['value'] == true) {
                selectednames.push(item['name']);
            }
        });
        console.log('Sendselected, selectednames: ' + selectednames.join(' '));
        $http({
            method : 'POST',
            url : 'api/table',
            data : selectednames
        }).then(
            function successCallback(response) {
                console.log('Sendselected, success: ', response);
            },
            function errorrCallback(response) {
                console.log('Sendselected, error: ', response);
            }
        );
    };
});
