'use strict';

/* Controllers */

var rankingApp = angular.module('rankingApp', []);


rankingApp.controller('RankingTableCtrl', function($scope, $http) {
    $scope.rankingTable = {headers : [], records : []};
    $scope.paginationParameters = {};
    $scope.yearSelect = null;
    $scope.rankingCheckList = null;
    $scope.paginationParameters = {};
    var updateLocalDataByResponse = function(responseData, scope) {
        console.log('Entry in updateLocalDataByResponse');

        var rankingTable = responseData['rankTable'];
        scope.rankingTable['headers'] = rankingTable[0];
        scope.rankingTable['records'] = rankingTable.slice(1);
        scope.tableWidth = scope.rankingTable.headers.length;

        console.log('updateLocalDataByResponse: after processed rankingTable');
        console.log('responseData.rankingsNamesList: ' + responseData.rankingsNamesList);
        console.log('responseData.yearsList: ' + responseData.yearsList);
        console.log('responseData.paginationParameters: ' + responseData.paginationParameters);
        console.log('after show responseData.paginationParameters');
        console.log('after after show responseData.paginationParameters');

        console.log('check yearSelect equal null');

        if ((scope.yearSelect === null) && (scope.rankingCheckList === null)) {
        //if ((!('yearSelect' in scope)) && (!('rankingCheckList' in scope))) {
            console.log("yearSelect not in scope and rankingCheckList not in scope");
            if (responseData.rankingsNamesList != null) {
                scope.rankingCheckList = [];
                scope.rankingCheckList = responseData.rankingsNamesList.map(function(rankingName) {
                    return {name : rankingName, value : false};
                });
            }

            if (responseData.yearsList != null) {
                var yearsList = responseData.yearsList;
                yearsList.sort();
                yearsList.reverse();

                scope.yearSelect = {
                    availableYears : [],
                    selectedYear : {id : 0, value : 0}
                };
                
                var maxYear = 0;
                var maxYearId = 0;
                yearsList.forEach(function(year, i, yearsList) {
                    scope.yearSelect.availableYears.push({id : i, value : year});
                    if (year > maxYear) {
                        maxYear = year;
                        maxYearId = i;
                    }
                });
                $scope.yearSelect.selectedYear.id = maxYearId;
                $scope.yearSelect.selectedYear.value = maxYear;
            }
        }
        else
        {
            console.log("yearSelect in scope or/and rankingCheckList in scope");
        }

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
            }
            else {
                console.log('recordsPerPageSelection already in scope.paginationParameters');
            }
            scope.paginationParameters.currentPageNum = responseData.paginationParameters.currentPageNum;
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

        if ('correlationMatrix' in responseData) {
            console.log('correlationMatrix is in responseData');
        }

        if (('correlationMatrix' in responseData) && (responseData.correlationMatrix != null)) {
            scope.correlationMatrix = responseData.correlationMatrix;
        }

        console.log('scope.correlationMatrix: ', scope.correlationMatrix);
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
        console.log('$scope.yearSelect.selectedYear.value: ' + $scope.yearSelect.selectedYear.value);
        if ((pageNum != $scope.paginationParameters.currentPageNum) && (pageNum >= $scope.paginationParameters.minPageNum) && (pageNum <= $scope.paginationParameters.totalPages)) {
            // send request
            var rankingCheckList = $scope.rankingCheckList;
            var selectedNames = [];
            console.log('Sendselected: selectedNames array declared');

            rankingCheckList.forEach(function(item, i, rankingCheckList) {
                if (item.value === true) {
                    selectedNames.push(item.name);
                }
                else {
                    console.log('Ranking name ' + item.name + ' not checked');
                }
            });

            $scope.requestData = {selectedRankingNames : selectedNames, selectedYear : $scope.yearSelect.selectedYear.value, currentPageNum : pageNum, recordsPerPage : $scope.paginationParameters.recordsPerPageSelection.selectedSize.value};
            console.log('request will be sended');

            $scope.retrieveTableData($scope.requestData);
            $scope.paginationParameters.currentPageNum = pageNum;
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

        var rankingCheckList = $scope.rankingCheckList;
        var selectedNames = [];

        rankingCheckList.forEach(function(item, i, rankingCheckList) {
            if (item.value === true) {
                selectedNames.push(item.name);
            }
        });

        $scope.requestData = {selectedRankingNames : selectedNames, selectedYear : $scope.yearSelect.selectedYear.value, currentPageNum : $scope.paginationParameters.currentPageNum, recordsPerPage : $scope.paginationParameters.recordsPerPageSelection.selectedSize.value}
        $scope.retrieveTableData($scope.requestData);
    };
});
