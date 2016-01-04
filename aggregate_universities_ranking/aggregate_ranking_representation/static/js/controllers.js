'use strict';

/* Controllers */

var rankingApp = angular.module('rankingApp', []);


rankingApp.controller('RankingTableCtrl', function($scope, $http) {
    $scope.rankingTable = {headers : [], records : []};
    $scope.paginationParameters = {};
    $scope.yearselect = null;
    $scope.rankingchecklist = null;
    $scope.paginationParameters = {};
    var updateLocalDataByResponse = function(responseData, scope) {
        console.log('Entry in updateLocalDataByResponse');

        var rankingTable = responseData['ranktable'];
        scope.rankingTable['headers'] = rankingTable[0];
        scope.rankingTable['records'] = rankingTable.slice(1);
        scope.tableWidth = scope.rankingTable.headers.length;

        console.log('updateLocalDataByResponse: after processed rankingTable');
        console.log('responseData.rankings_names_list: ' + responseData.rankings_names_list);
        console.log('responseData.years_list: ' + responseData.years_list);
        console.log('responseData.paginationParameters: ' + responseData.paginationParameters);
        console.log('after show responseData.paginationParameters');
        console.log('after after show responseData.paginationParameters');

        console.log('check yearselect equal null');

        /*if (scope.yearselect === null) {
            console.log('yearselect === null');
        }
        else {
            console.log('yearselect !== null');
        }

        console.log('check rankingchecklist equal null');
        if (scope.rankingchecklist === null) {
            console.log('rankingchecklist === null');
        }
        else {
            console.log('rankingchecklist !== null');
        }

        if ((scope.yearselect === null) && (scope.rankingchecklist === null)) {
            console.log('(scope.yearselect === null) && (scope.rankingchecklist === null)');
        }
        else {

            console.log('(scope.yearselect !== null) || (scope.rankingchecklist !== null)');
        }*/
        if ((scope.yearselect === null) && (scope.rankingchecklist === null)) {
        //if ((!('yearselect' in scope)) && (!('rankingchecklist' in scope))) {
            console.log("yearselect not in scope and rankingchecklist not in scope");
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
            console.log("yearselect in scope or/and rankingchecklist in scope");
        }

        console.log('updateLocalDataByResponse, just before paginationParameters processed');
        if ('paginationParameters' in responseData) {
        //if (scope.paginationParameters === {}) {
            console.log('paginationParameters are in responseData');
            if (!('recordsPerPageSelection' in scope.paginationParameters)) {
                console.log('recordsPerPageSelection not in scope.paginationParameters');
                var recordsPerPageSelectionList = responseData.paginationParameters.recordsPerPageSelectionList;
                recordsPerPageSelectionList.sort(function(a, b){ return a - b;});
                scope.paginationParameters.recordsPerPageSelection = {
                    availableSizes : [],
                    selectedSize : {id : 0, value : recordsPerPageSelectionList[0]}
                };
                recordsPerPageSelectionList.forEach(function(size, i, recordsPerPageSelectionList) {
                    scope.paginationParameters.recordsPerPageSelection.availableSizes.push({id : i, value : size});
                });

                console.log('scope.paginationParameters.recordsPerPageSelection.availableSizes: ' + scope.paginationParameters.recordsPerPageSelection.availableSizes.join(' '));
            }
            else {
                console.log('recordsPerPageSelection already in scope.paginationParameters');
            }
            console.log('in updateLocalDataByResponse, responseData.paginationParameters.currentPageNum: ' + responseData.paginationParameters.currentPageNum);
            scope.paginationParameters.currentPageNum = responseData.paginationParameters.currentPageNum;
            console.log('in updateLocalDataByResponse, scope.paginationParameters.currentPageNum: ' + scope.paginationParameters.currentPageNum);
            scope.paginationParameters.totalTableRecords = responseData.paginationParameters.totalTableRecords;
            scope.paginationParameters.totalPages = responseData.paginationParameters.totalPages;
            scope.paginationParameters.minPageNum = 1;
            console.log('scope.paginationParameters.totalPages: ' + scope.paginationParameters.totalPages);
            var pagesNumberArray = [];
            for (var i = 1; i <= scope.paginationParameters.totalPages; i++) {
                pagesNumberArray.push(i);
            }
            scope.paginationParameters.pagesNumberArray = pagesNumberArray;
            console.log('pagesNumberArray: ' + scope.paginationParameters.pagesNumberArray.join(' '));
        }
        else {
            console.log('paginationParameters are\'nt in responseData');
        }
    };

    $scope.requestData =  {selectedRankingNames : null, selectedYear : null, currentPage : null, recordsPerPage : null}
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
    };

    $scope.goToPage = function(pageNum) {
        console.log('pageNum: ' + pageNum);
        console.log('$scope.paginationParameters.totalTableRecords: ' + $scope.paginationParameters.totalTableRecords);
        console.log('$scope.paginationParameters.recordsPerPageSelection.selectedSize.value: ' + $scope.paginationParameters.recordsPerPageSelection.selectedSize.value);
        console.log('$scope.yearselect.selectedYear.value: ' + $scope.yearselect.selectedYear.value);
        if ((pageNum != $scope.paginationParameters.currentPageNum) && (pageNum >= $scope.paginationParameters.minPageNum) && (pageNum <= $scope.paginationParameters.totalPages)) {
            // send request
            var rankingchecklist = $scope.rankingchecklist;
            var selectednames = [];
            console.log('Sendselected: selectednames array declared');

            rankingchecklist.forEach(function(item, i, rankingchecklist) {
                if (item.value === true) {
                    selectednames.push(item.name);
                    console.log('Ranking name ' + item.name + ' checked');
                }
                else {
                    console.log('Ranking name ' + item.name + ' not checked');
                }
            });

            console.log('selectednames: ' + selectednames.join(' '));

            //$scope.requestData = {selectedRankingNames : selectednames, selectedYear : $scope.yearselect.selectedYear.value, currentPageNum : $scope.paginationParameters.currentPageNum, recordsPerPage : $scope.paginationParameters.recordsPerPageSelection.selectedSize.value};
            $scope.requestData = {selectedRankingNames : selectednames, selectedYear : $scope.yearselect.selectedYear.value, currentPageNum : pageNum, recordsPerPage : $scope.paginationParameters.recordsPerPageSelection.selectedSize.value};
            console.log('request will be sended');

            $scope.retrieveTableData($scope.requestData);
            $scope.paginationParameters.currentPageNum = pageNum;
            console.log('after call retrieveTableData and assign pageNum, $scope.paginationParameters.currentPageNum: ' + $scope.paginationParameters.currentPageNum);
        }
        else {
            console.log('pageNum not allowed, request not will sended');
        }

        console.log('$scope.paginationParameters.currentPageNum: ' + $scope.paginationParameters.currentPageNum);
    };

    $scope.goToNextPage = function() {
        console.log('Entry in goToNextPage');
        $scope.goToPage($scope.paginationParameters.currentPageNum + 1);
    };

    $scope.goToPrevPage = function() {
        console.log('Entry in goToPrevPage');
        $scope.goToPage($scope.paginationParameters.currentPageNum - 1);
    };

    $scope.goToFirstPage = function() {
        $scope.goToPage($scope.paginationParameters.minPageNum);
    };

    $scope.goToLastPage = function() {
        $scope.goToPage($scope.paginationParameters.totalPages);
    };

    $scope.nextPageDisabled = function() {
        return $scope.paginationParameters.currentPageNum === $scope.paginationParameters.totalPages ? 'disabled' : '';
    };

    $scope.prevPageDisabled = function() {
        return $scope.paginationParameters.currentPageNum === $scope.paginationParameters.minPageNum ? 'disabled' : '';
    };

    $scope.firstPageDisabled = function() {
        return $scope.paginationParameters.currentPageNum === $scope.paginationParameters.minPageNum ? 'disabled' : '';
    }

    $scope.lastPageDisabled = function() {
        return $scope.paginationParameters.currentPageNum === $scope.paginationParameters.totalPages ? 'disabled' : '';
    }

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

        $scope.requestData = {selectedRankingNames : selectednames, selectedYear : $scope.yearselect.selectedYear.value, currentPageNum : $scope.paginationParameters.currentPageNum, recordsPerPage : $scope.paginationParameters.recordsPerPageSelection.selectedSize.value}
        console.log('$scope.requestData.selectedRankingNames: ' + $scope.requestData.selectedRankingNames + ', $scope.requestData.selectedYear: ' + $scope.requestData.selectedYear);
        $scope.retrieveTableData($scope.requestData);
    };
});
