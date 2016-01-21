'use strict';

/* Controllers */

var rankingApp = angular.module('rankingControllers', []); 


var checkArrayEquality = function(array_1, array_2) {
    if (array_1.length !== array_2.length) {
        return false;
    }
    return array_1.sort().join() === array_2.sort().join();
}

rankingApp.controller('RankingTableController', function($scope, $http) {

    $scope.setActiveNavItem(2);

    //var paginationParameters = {};

    $scope.rankingTable = {headers : [], records : []};
    $scope.paginationParameters = {};
    $scope.yearSelect = null;
    $scope.rankingCheckList = null;
    $scope.paginationParameters = {};
    $scope.currentSelectedRankNames = [];
    $scope.currentSelectedYear = null;

    $scope.getSelectedNames = function(scope) {
        var rankingCheckList = scope.rankingCheckList;
        var selectedNames = [];

        rankingCheckList.forEach(function(item, i, rankingCheckList) {
            if (item.value === true) {
                selectedNames.push(item.name);
            }
        });

        return selectedNames;
    }

    $scope.prepareRequestData = function(scope) {

        var selectedNames = scope.getSelectedNames(scope);

        scope.requestData = {selectedRankingNames : selectedNames, selectedYear : scope.yearSelect.selectedYear.value, currentPageNum : scope.paginationParameters.currentPageNum, recordsPerPage : scope.paginationParameters.recordsPerPageSelection.selectedSize.value, needsToBeUpdated : false};

        if ((scope.currentSelectedYear != scope.yearSelect.selectedYear.value) || (checkArrayEquality(scope.currentSelectedRankNames, selectedNames) === false)) {
            scope.requestData.needsToBeUpdated = true;
        }
        else {
            scope.requestData.needsToBeUpdated = false;
        }
    };


    var updateLocalDataByResponse = function(responseData, scope) {

        var currentSelectedYearChanged = false;
        var currentSelectedRankNamesChanged = false;

        var rankingTable = responseData['rankTable'];
        scope.rankingTable['headers'] = rankingTable[0];
        scope.rankingTable['records'] = rankingTable.slice(1);
        scope.tableWidth = scope.rankingTable.headers.length;

        if ((scope.yearSelect === null) && (scope.rankingCheckList === null)) {
        //if ((!('yearSelect' in scope)) && (!('rankingCheckList' in scope))) {
            if (responseData.rankingsNamesList != null) {
                scope.rankingCheckList = [];
                scope.rankingCheckList = responseData.rankingsNamesList.map(function(rankingName) {
                    return {name : rankingName, value : false};
                });

                if (checkArrayEquality(scope.currentSelectedRankNames, responseData.rankingsNamesList) === false) {
                    scope.currentSelectedRankNames = responseData.rankingsNamesList;
                    currentSelectedRankNamesChanged = true;
                }
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
                scope.yearSelect.selectedYear.id = maxYearId;
                scope.yearSelect.selectedYear.value = maxYear;
                if (scope.currentSelectedYear != responseData.selectedYear) {
                    scope.currentSelectedYear = responseData.selectedYear;
                    currentSelectedYearChanged = true;
                }
            }
        }

        if (currentSelectedYearChanged || currentSelectedRankNamesChanged) {
            //console.log('currentSelectedYearChanged || currentSelectedRankNamesChanged');
            /*if (('correlationMatrix' in responseData) && (responseData.correlationMatrix != null)) {
                scope.correlationMatrix = responseData.correlationMatrix;
                scope.requestData.needsToBeUpdated = false;
                console.log('scope.requestData.needsToBeUpdated: ' + scope.responseData.needsToBeUpdated);
            }*/
            //console.log('scope.correlationMatrix: ', scope.correlationMatrix);
        }
        else {
            //console.log('currentSelectedYearChanged === false && currentSelectedRankNamesChanged === false');

        }
        

        if ('paginationParameters' in responseData) {
            if (!('recordsPerPageSelection' in scope.paginationParameters)) {

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
                ;
            }

            scope.paginationParameters.currentPageNum = responseData.paginationParameters.currentPageNum;
            scope.paginationParameters.totalTableRecords = responseData.paginationParameters.totalTableRecords;
            scope.paginationParameters.totalPages = responseData.paginationParameters.totalPages;
            scope.paginationParameters.minPageNum = 1;
            var pagesNumberArray = [];
            for (var i = 1; i <= scope.paginationParameters.totalPages; i++) {
                pagesNumberArray.push(i);
            }
            scope.paginationParameters.pagesNumberArray = pagesNumberArray;

            var pagesNumberArray = scope.paginationParameters.pagesNumberArray;
            var firstPageIndexInPagesArray = scope.paginationParameters.minPageNum - 1;
            var lastPageIndexInPagesArray = scope.paginationParameters.totalPages - 1;
            var currentPageIndexInPagesArray = scope.paginationParameters.currentPageNum - 1;
            var firstCurrentDistance = currentPageIndexInPagesArray - firstPageIndexInPagesArray;
            var currentLastDistance = lastPageIndexInPagesArray - currentPageIndexInPagesArray;
            var adjoinedToMarginPagesNum = 2;
            var adjoinedToCurrentPagesNum = 2;
            var leftNumsArray = pagesNumberArray.slice(firstPageIndexInPagesArray, currentPageIndexInPagesArray);
            var rightNumsArray = pagesNumberArray.slice(currentPageIndexInPagesArray + 1, lastPageIndexInPagesArray);
            var minNonShowingPagesNum = 2;
            var maxShowAllPagesNum = adjoinedToMarginPagesNum + adjoinedToCurrentPagesNum + minNonShowingPagesNum - 1;
            var adjoinedToFirstPages = [];
            var leftAdjoinedToCurrentPages = [];
            var adjoinedToLastPages = [];
            var rightAdjoinedToCurrentPages = [];
            var showedPagesNumsArray = [];

            if (firstCurrentDistance > maxShowAllPagesNum) {
                adjoinedToFirstPages = pagesNumberArray.slice(firstPageIndexInPagesArray, adjoinedToMarginPagesNum);
                leftAdjoinedToCurrentPages = pagesNumberArray.slice(currentPageIndexInPagesArray - adjoinedToCurrentPagesNum, currentPageIndexInPagesArray);
                leftNumsArray = adjoinedToFirstPages.concat('\u2026');
                leftNumsArray = leftNumsArray.concat(leftAdjoinedToCurrentPages);
            }

            if (currentLastDistance > maxShowAllPagesNum) {
                adjoinedToLastPages = pagesNumberArray.slice(lastPageIndexInPagesArray - adjoinedToMarginPagesNum + 1, lastPageIndexInPagesArray + 1);
                rightAdjoinedToCurrentPages = pagesNumberArray.slice(currentPageIndexInPagesArray + 1, currentPageIndexInPagesArray + adjoinedToCurrentPagesNum + 1);
                rightNumsArray = rightAdjoinedToCurrentPages.concat('\u2026');
                rightNumsArray = rightNumsArray.concat(adjoinedToLastPages);
            }

            showedPagesNumsArray = showedPagesNumsArray.concat(leftNumsArray);
            showedPagesNumsArray = showedPagesNumsArray.concat(scope.paginationParameters.currentPageNum);
            showedPagesNumsArray = showedPagesNumsArray.concat(rightNumsArray);

            scope.paginationParameters.showedPagesNumsArray = showedPagesNumsArray;
        }
        else {
            console.log('paginationParameters are\'nt in responseData');
        }


        if (('correlationMatrix' in responseData) && (responseData.correlationMatrix != null)) {
           scope.correlationMatrix = responseData.correlationMatrix;
        }


        if (('aggregateRankingCsvFileDownloadPath' in responseData) && (responseData.aggregateRankingCsvFileDownloadPath !== null)) {
            $scope.aggregateRankingCsvFileDownloadPath = responseData.aggregateRankingCsvFileDownloadPath;
        }
    };

    $scope.requestData =  {selectedRankingNames : null, selectedYear : null, currentPage : null, recordsPerPage : null, needsToBeUpdated : false}

    $scope.retrieveTableData = function(requestData) {

        $scope.spinner.on();
        $http({
            method : 'POST',
            url : 'rest/table',
            data : requestData
        }).then(
            function successCallback(response) {
                //console.log('retrieveTableData, success: ', response);
                $scope.table = response.data;
                updateLocalDataByResponse(response.data, $scope);
                $scope.spinner.off();
            },
            function errorrCallback(response) {
                //console.log('retrieveTableData, error: ', response);
                $scope.spinner.off();
            }
        );
    };

    $scope.goToPage = function(pageNum) {

        if ((pageNum != $scope.paginationParameters.currentPageNum) && (pageNum >= $scope.paginationParameters.minPageNum) && (pageNum <= $scope.paginationParameters.totalPages)) {
            
            $scope.prepareRequestData($scope);
            $scope.requestData.currentPageNum = pageNum;

            $scope.retrieveTableData($scope.requestData);
            $scope.paginationParameters.currentPageNum = pageNum;
        }
    };

    $scope.goToNextPage = function() {
        $scope.goToPage($scope.paginationParameters.currentPageNum + 1);
    };

    $scope.goToPrevPage = function() {
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
        $scope.requestData.needsToBeUpdated = true;
        $scope.retrieveTableData($scope.requestData);
    }

    $scope.sendSelected = function() {

        $scope.prepareRequestData($scope);
        $scope.retrieveTableData($scope.requestData);
    };

    function openSaveAsDialog(filename, content, mediaType) {
        console.log('Entry in openSaveAsDialog');
        var blob = new Blob([content], {type : mediaType});
        saveAs(blob, filename);
    }

    $scope.downloadFile = function(scope, dataType, fileType) {
        var selectedNames = scope.getSelectedNames(scope);
        var requestData = {selectedRankingNames : selectedNames, selectedYear : scope.yearSelect.selectedYear.value, dataType: dataType, fileType : fileType};
        $http({
            method : 'POST',
            url : 'rest/download',
            data : requestData
        }).then(
            function successCallback(response) {
                var data = response.data;
                openSaveAsDialog('ranktable.csv', data,'text/csv;charset=utf-8;');
            },
            function errorrCallback(response) {
                console.log('downloadFile, error: ', response);
                //$scope.spinner.off();
            }
        );
    };

    $scope.downloadTableAsXLS = function() {
        //$scope.downloadFile($scope, 'rankTable', 'xls');
        $scope.downloadFile($scope, 'rankTable', 'csv');
    };
});

rankingApp.controller('StartController', function($scope) {

    $scope.setActiveNavItem(1);
    $scope.methodologyText = 'Many, many sentences about methodology with terrible formulas...' //Must get methodology text from database. User must can possibility login and edit methodology text.
});

rankingApp.controller('NavigationController', function($scope) {

    var navClasses;

    function initNavClasses() {
        navClasses = ['', ''];
    }

    $scope.getNavClass = function(navItemNum) {
        return navClasses[navItemNum];
    };
    
    $scope.setActiveNavItem = function(navItemNum) {
        initNavClasses();
        navClasses[navItemNum] = 'active';
    };

    initNavClasses();
    $scope.setActiveNavItem(1);
});
