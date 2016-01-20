'use strict';

/* Controllers */

//var rankingApp = angular.module('rankingApp', []); //This strongly need comment if loaded app.js !!!
var rankingApp = angular.module('rankingControllers', []); //This strongly need unkomment If loaded app.js !!!


var checkArrayEquality = function(array_1, array_2) {
    if (array_1.length !== array_2.length) {
        return false;
    }
    return array_1.sort().join() === array_2.sort().join();
}

rankingApp.controller('RankingTableController', function($scope, $http) {

    //console.log('Entry in RankingTableController');
    if ('setActiveNavItem' in $scope) {
        //console.log('RankingTableController, setActiveNavItem is in $scope');
        ;
    }
    else {
        //console.log('RankingTableController, setActiveNavItem is not in $scope');
        ;
    }

    $scope.setActiveNavItem(2);

    
    //var paginationParameters = {};


    $scope.rankingTable = {headers : [], records : []};
    $scope.paginationParameters = {};
    $scope.yearSelect = null;
    $scope.rankingCheckList = null;
    $scope.paginationParameters = {};
    $scope.currentSelectedRankNames = [];
    $scope.currentSelectedYear = null;

    $scope.prepareRequestData = function(scope) {
        //console.log('Entry in prepareRequestData');
        var rankingCheckList = scope.rankingCheckList;
        var selectedNames = [];

        rankingCheckList.forEach(function(item, i, rankingCheckList) {
            if (item.value === true) {
                selectedNames.push(item.name);
            }
        });

        //console.log('prepareRequestData, just after add items to selectedNames');

        scope.requestData = {selectedRankingNames : selectedNames, selectedYear : scope.yearSelect.selectedYear.value, currentPageNum : scope.paginationParameters.currentPageNum, recordsPerPage : scope.paginationParameters.recordsPerPageSelection.selectedSize.value, needsToBeUpdated : false};

        //console.log('prepareRequestData, just after set scope.requestData');

        if ((scope.currentSelectedYear != scope.yearSelect.selectedYear.value) || (checkArrayEquality(scope.currentSelectedRankNames, selectedNames) === false)) {
            scope.requestData.needsToBeUpdated = true;
        }
        else {
            scope.requestData.needsToBeUpdated = false;
        }
    };


    var updateLocalDataByResponse = function(responseData, scope) {
        //console.log('Entry in updateLocalDataByResponse');

        var currentSelectedYearChanged = false;
        var currentSelectedRankNamesChanged = false;

        var rankingTable = responseData['rankTable'];
        scope.rankingTable['headers'] = rankingTable[0];
        scope.rankingTable['records'] = rankingTable.slice(1);
        scope.tableWidth = scope.rankingTable.headers.length;

        if ((scope.yearSelect === null) && (scope.rankingCheckList === null)) {
        //if ((!('yearSelect' in scope)) && (!('rankingCheckList' in scope))) {
            //console.log("yearSelect not in scope and rankingCheckList not in scope");
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
        else
        {
            //console.log("yearSelect in scope or/and rankingCheckList in scope");
            ;
        }
        
        //console.log('responseData.correlationMatrix: ' + responseData.correlationMatrix);

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
        
        //console.log('Just before process paginationParameters: ');

        if ('paginationParameters' in responseData) {
        //if (scope.paginationParameters === {}) {
            //console.log('paginationParameters are in responseData');
            if (!('recordsPerPageSelection' in scope.paginationParameters)) {
                //console.log('recordsPerPageSelection not in scope.paginationParameters');
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
                //console.log('recordsPerPageSelection already in scope.paginationParameters');
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

            console.log('leftNumsArray before check firstCurrentDistance: ');
            console.log(leftNumsArray.join(' '));
            if (firstCurrentDistance > maxShowAllPagesNum) {
                adjoinedToFirstPages = pagesNumberArray.slice(firstPageIndexInPagesArray, adjoinedToMarginPagesNum);
                leftAdjoinedToCurrentPages = pagesNumberArray.slice(currentPageIndexInPagesArray - adjoinedToCurrentPagesNum, currentPageIndexInPagesArray);
                leftNumsArray = adjoinedToFirstPages.concat('\u2026');
                leftNumsArray = leftNumsArray.concat(leftAdjoinedToCurrentPages);
            }
            else {
                ;
            }
            console.log('leftNumsArray after check firstCurrentDistance: ');
            console.log(leftNumsArray.join(' '));

            console.log('rightNumsArray before check currentLastDistance: ');
            console.log(rightNumsArray.join(' '));
            if (currentLastDistance > maxShowAllPagesNum) {
                adjoinedToLastPages = pagesNumberArray.slice(lastPageIndexInPagesArray - adjoinedToMarginPagesNum, lastPageIndexInPagesArray + 1);
                rightAdjoinedToCurrentPages = pagesNumberArray.slice(currentPageIndexInPagesArray + 1, currentPageIndexInPagesArray + adjoinedToCurrentPagesNum + 1);
                rightNumsArray = rightAdjoinedToCurrentPages.concat('\u2026');
                rightNumsArray = rightNumsArray.concat(adjoinedToLastPages);
            }
            else {
                ;
            }
            console.log('rightNumsArray after check currentLastDistance: ');
            console.log(rightNumsArray.join(' '));

            showedPagesNumsArray = showedPagesNumsArray.concat(leftNumsArray);
            showedPagesNumsArray = showedPagesNumsArray.concat(scope.paginationParameters.currentPageNum);
            showedPagesNumsArray = showedPagesNumsArray.concat(rightNumsArray);

            scope.paginationParameters.showedPagesNumsArray = showedPagesNumsArray;
            console.log('showedPagesNumsArray: ' + scope.paginationParameters.showedPagesNumsArray.join(' '));
        }
        else {
            //console.log('paginationParameters are\'nt in responseData');
            ;
        }


        if (('correlationMatrix' in responseData) && (responseData.correlationMatrix != null)) {
           scope.correlationMatrix = responseData.correlationMatrix;
        }

        //console.log('scope.correlationMatrix: ', scope.correlationMatrix);

        if (('aggregateRankingCsvFileDownloadPath' in responseData) && (responseData.aggregateRankingCsvFileDownloadPath !== null)) {
            $scope.aggregateRankingCsvFileDownloadPath = responseData.aggregateRankingCsvFileDownloadPath;
        }
    };

    $scope.requestData =  {selectedRankingNames : null, selectedYear : null, currentPage : null, recordsPerPage : null, needsToBeUpdated : false}

    $scope.retrieveTableData = function(requestData) {
        //console.log('retrieveTableData: $scope.requestData.selectedRankingNames: ' + $scope.requestData.selectedRankingNames + ', $scope.requestData.selectedYear: ' + $scope.requestData.selectedYear);
        if ('spinner' in $scope) {
            //console.log('spinner in scope');
            ;
        }
        else {
            //console.log('spinner not in scope');
            ;
        }
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
        //console.log('pageNum: ' + pageNum);
        if ((pageNum != $scope.paginationParameters.currentPageNum) && (pageNum >= $scope.paginationParameters.minPageNum) && (pageNum <= $scope.paginationParameters.totalPages)) {
            
            $scope.prepareRequestData($scope);
            $scope.requestData.currentPageNum = pageNum;
            //console.log('request will be sended');

            //console.log('goToPage, pageNum: ' + pageNum);
            $scope.retrieveTableData($scope.requestData);
            $scope.paginationParameters.currentPageNum = pageNum;
            //console.log('goToPage, $scope.paginationParameters.currentPageNum: ' + $scope.paginationParameters.currentPageNum);
        }
        else {
            //console.log('pageNum not allowed, request not will sended');
            ;
        }

        //console.log('$scope.paginationParameters.currentPageNum: ' + $scope.paginationParameters.currentPageNum);
    };

    $scope.goToNextPage = function() {
        //console.log('Entry in goToNextPage');
        $scope.goToPage($scope.paginationParameters.currentPageNum + 1);
    };

    $scope.goToPrevPage = function() {
        //console.log('Entry in goToPrevPage');
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
        //console.log('Entry in sendSelected');

        $scope.prepareRequestData($scope);

        //console.log('Before call retrieveTableData');
        $scope.retrieveTableData($scope.requestData);
    };
});

rankingApp.controller('StartController', function($scope) {
    //console.log('Entry in StartController');
    if ('setActiveNavItem' in $scope) {
        //console.log('StartController, setActiveNavItem is in $scope');
        ;
    }
    else {
        //console.log('StartController, setActiveNavItem is not in $scope');
        ;
    }
    $scope.setActiveNavItem(1);
    $scope.methodologyText = 'Many, many sentences about methodology with terrible formulas...' //Must get methodology text from database. User must can possibility login and edit methodology text.
});

rankingApp.controller('NavigationController', function($scope) {
    //console.log('Entry in NavigationController');

    var navClasses;

    function initNavClasses() {
        //console.log('Entry in initNavClasses');
        navClasses = ['', ''];
    }

    $scope.getNavClass = function(navItemNum) {
        //console.log('Entry in getNavClass, navItemNum = ' + navItemNum);
        return navClasses[navItemNum];
    };
    
    $scope.setActiveNavItem = function(navItemNum) {
        //console.log('Entry in setActiveNavItem, navItemNum = ' + navItemNum);
        initNavClasses();
        navClasses[navItemNum] = 'active';
    };

    initNavClasses();
    $scope.setActiveNavItem(1);
});
