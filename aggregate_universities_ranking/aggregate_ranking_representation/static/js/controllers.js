'use strict';

/* Controllers */

var rankingApp = angular.module('rankingApp', []);


rankingApp.controller('RankingTableCtrl', function($scope, $http) {
    $scope.rankingTable = {headers : [], records : []};
    $scope.paginationParameters = {};
    var updateLocalDataByResponse = function(responseData, scope) {
        console.log('Entry in updateLocalDataByResponse');

        var rankingTable = responseData['ranktable'];
        scope.rankingTable['headers'] = rankingTable[0];
        scope.rankingTable['records'] = rankingTable.slice(1);
        scope.tableWidth = scope.rankingTable.headers.length;

        if (!('yearselect' in scope) && !('rankingchecklist' in scope)) {
            if (responseData.rankings_names_list != null) {
                scope.rankingchecklist = [];
                scope.rankingchecklist = responseData.rankings_names_list.map(function(rankingName) {
                    return {name : rankingName, value : false};
                });
            }

            if (responseData.years_list != null) {
                var yearslist = responseData.years_list;
                yearslist.sort();
                yearslist.reverse();

                scope.yearselect = {
                    availableYears : [],
                    selectedYear : {id : 0, value : 0}
                };
                
                var maxYear = 0;
                var maxYearId = 0;
                yearslist.forEach(function(year, i, yearslist) {
                    scope.yearselect.availableYears.push({id : i, value : year});
                    if (year > maxYear) {
                        maxYear = year;
                        maxYearId = i;
                    }
                });
                $scope.yearselect.selectedYear.id = maxYearId;
                $scope.yearselect.selectedYear.value = maxYear;
            }
        }
        else
        {
            conslole.log("yearselect in scope or/and rankingchecklist in scope");
        }

        if ('paginationParameters' in responseData) {
            console.log('paginationParameters are in responseData');
            if (!('recordsPerPageSelection' in scope.paginationParameters)) {
                console.log('recordsPerPageSelection not in scope.paginationParameters');
                var recordsPerPageSelectionList = responseData.paginationParameters.recordsPerPageSelectionList;
                recordsPerPageSelectionList.sort(function(a, b){ return a - b;});
                scope.recordsPerPageSelection = {
                    availableSizes : [],
                    selectedSize : {id : 0, value : recordsPerPageSelectionList[0]}
                };
                recordsPerPageSelectionList.forEach(function(size, i, recordsPerPageSelectionList) {
                    scope.recordsPerPageSelection.availableSizes.push({id : i, value : size});
                });

                console.log('scope.recordsPerPageSelection.recordsPerPageSelection.availableSizes: ' + scope.recordsPerPageSelection.availableSizes.join(' '));
            }
            else {
                console.log('recordsPerPageSelection already in scope.paginationParameters');
            }
            scope.paginationParameters.currentPageNum = responseData.paginationParameters.currentPageNum;
            scope.paginationParameters.totalTableRecords = responseData.paginationParameters.totalTableRecords;
            scope.paginationParameters.totalPages = responseData.paginationParameters.totalPages;
            console.log('scope.paginationParameters.totalPages: ' + scope.paginationParameters.totalPages);
            var pagesNumberArray = [];
            for (var i = 1; i <= scope.paginationParameters.totalPages; i++) {
                pagesNumberArray.push(i);
            }
            scope.paginationParameters.pagesNumberArray = pagesNumberArray;
            console.log('pagesNumberArray: ' + scope.paginationParameters.pagesNumberArray.join(' '));
            scope.paginationParameters.prevPage = responseData.paginationParameters.prevPage;
            scope.paginationParameters.nextPage = responseData.paginationParameters.nextPage;
        }
        else {
            console.log('paginationParameters are\'nt in responseData');
        }
    };

    $scope.requestData =  {selectedRankingNames : null, selectedYear : null}
    $scope.retrieveTableData = function(requestData) {
        console.log('retrieveTableData: $scope.requestData.selectedRankingNames: ' + $scope.requestData.selectedRankingNames + ', $scope.requestData.selectedYear: ' + $scope.requestData.selectedYear);

        $http({
            method : 'POST',
            url : 'api/table',
            data : requestData
        }).then(
            function successCallback(response) {
                console.log('retrieveTableData, success: ', response);
                $scope.table = response.data;
                updateLocalDataByResponse(response.data, $scope);
                //console.log('$scope.table[0]: ' + $scope.table[0].join(' '));
            },
            function errorrCallback(response) {
                console.log('retrieveTableData, error: ', response);
            }
        );
    }

    $scope.goToPage = function(pageNum) {
        console.log('pageNum: ' + pageNum);
    };

    if ($scope.requestData.selectedRankingNames === null && $scope.requestData.selectedYear === null) {
        $scope.retrieveTableData($scope.requestData);
    }
});


rankingApp.controller('RankingCheckController', function($scope, $http) {
    $scope.sendselected = function() {
        console.log('Entry in sendselected');

        var rankingchecklist = $scope.rankingchecklist;
        var selectednames = [];
        console.log('Sendselected: selectednames array declared');

        rankingchecklist.forEach(function(item, i, rankingchecklist) {
            if (item.value === true) {
                selectednames.push(item.name);
            }
        });
        console.log('Sendselected, selectednames: ' + selectednames.join(' '));

        $scope.requestData = {selectedRankingNames : selectednames, selectedYear : $scope.yearselect.selectedYear.value}
        console.log('$scope.requestData.selectedRankingNames: ' + $scope.requestData.selectedRankingNames + ', $scope.requestData.selectedYear: ' + $scope.requestData.selectedYear);
        $scope.retrieveTableData($scope.requestData);
    };
});
