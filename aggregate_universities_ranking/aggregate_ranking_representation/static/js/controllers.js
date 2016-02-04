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

    function assembleFileName(prefix, selectedRankingNames, year) {
        var filename = prefix;

        selectedRankingNames.forEach(function(item, i, selectedRankingNames) {
            filename = filename + '_' + item;
        });

        filename = filename + '_' + year;

        return filename.toLowerCase();
    }

    function saveFile(dataType, selectedNames, selectedYear, fileType, fileContent) {
        if (selectedNames.length == 0) {
            var rankingCheckList = $scope.rankingCheckList;
            rankingCheckList.forEach(function(item, i, rankingCheckList) {
                selectedNames.push(item.name);
            });
        }
        else {
            console.log('saveFile, selectedNames !== []');
        }
        selectedNames.sort();
        var fileName = assembleFileName(dataType, selectedNames, selectedYear);
        if (fileType === 'csv') {
            openSaveAsDialog(fileName + '.csv', fileContent,'text/csv;charset=utf-8;');
        }
        else if (fileType === 'xls') {
            openSaveAsDialog(fileName + '.xls', fileContent,'application/vnd.ms-excel;charset=utf-8');
        }
    }
    
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
            responseType: 'arraybuffer',
            data : requestData
        }).then(
            function successCallback(response) {
                var data = response.data;
                //console.log(data);
                console.log(md5(data));
                saveFile(dataType, requestData.selectedRankingNames, requestData.selectedYear, fileType, data);
            },
            function errorrCallback(response) {
                console.log('downloadFile, error: ', response);
            }
        );
    };

    $scope.downloadTableAsCSV = function() {
        $scope.downloadFile($scope, 'rankTable', 'csv');
    };

    $scope.downloadTableAsXLS = function() {
        $scope.downloadFile($scope, 'rankTable', 'xls');
    };

    $scope.downloadCorrelationMatrixAsCSV = function() {
        $scope.downloadFile($scope, 'correlation', 'csv');
    };

    $scope.downloadCorrelationMatrixAsXLS = function() {
        $scope.downloadFile($scope, 'correlation', 'xls');
    };

});

rankingApp.controller('StartController', function($scope) {

    $scope.setActiveNavItem(1);
    $scope.methodologyText = 'Many, many sentences about methodology with terrible formulas...' //Must get methodology text from database. User must can possibility login and edit methodology text.
});

rankingApp.controller('NavigationController', function($scope) {

    var navClasses;

    $scope.langSelect = {
        availableLanguages : [{id : 0, value : 'En'}, {id : 1, value : 'Ру'}],
        selectedLang : {id : 0, value : 'En'}
    };

    var langEnValues = {selectLanguageTitle : 'Select Language', methodologyTitle : 'Methodology', goToTitle : 'Go to', homeNavigationTitle : 'Home', rankingTableNavigationTitle : 'Ranking Table', rankingTablePageTitle : 'Aggregated rankings table', downloadAsCSVButtonTitle : 'Download as csv', downloadAsXLSButtonTitle : 'Download as excel', selectRankingsNamesTitle : 'Select rankings', selectYearTitle : 'Select year', selectPerPageTitle : 'Table records per page', applyButtonTitle : 'Apply', showCorrelationMatrixButtonTitle : 'Show correlation matrix', hideCorrelationMatrixButtonTitle : 'Hide correlation matrix', correlationMatrixTitle : 'Correlation matrix'};

    var langRuValues = {selectLanguageTitle: 'Выбрать язык', methodologyTitle : 'Методология', goToTitle : 'Перейти', homeNavigationTitle : 'Главная', rankingTableNavigationTitle : 'Таблица рейтингов', rankingTablePageTitle : 'Таблица рейтингов', downloadAsCSVButtonTitle : 'Сохранить как csv файл', downloadAsXLSButtonTitle : 'Сохранить как excel файл', selectRankingsNamesTitle : 'Выбрать рейтинги', selectYearTitle : 'Выбрать год', selectPerPageTitle : 'Количество записей в таблице на страницу', applyButtonTitle : 'Применить', showCorrelationMatrixButtonTitle : 'Кроскорреляционная матрица', hideCorrelationMatrixButtonTitle : 'Скрыть кроскорреляционную матрицу', correlationMatrixTitle : 'Кроскорреляционная матрица'};

    //var methodologyEn = '$R_i$ и $R_j$, длинною соответственно $l_i$ и $l_j$';
    //var methodologyEn = '$R_i$ и $R_j$, длинною соответственно $l_i$ и $l_j$';
    //

    var ents_ = { nwarr: '\u2196', swarr: '\u2199' };
    console.log('before jqMath call');
    var translateToMath = M.sToMathE('$$∑↙{i=0}↖n i={n(n+1)}/2$$', true);
    console.log(translateToMath);
    console.log(typeof(translateToMath));
    console.log(typeof('abc'));
    //var methodologyEn = translateToMath;
    var methodologyEn = '$R_i$ и $R_j$, длинною соответственно $l_i$ и $l_j$';
    var methodologyEnMath = 'R_i\\:и\\:R_j,\\text\" длинною соответственно \" l_i и l_j';

    methodologyEnMath = methodologyEnMath.replace(/&([-#.\w]+);|\\([a-z]+)(?: |(?=[^a-z]))/ig,
            function(s, e, m) {
                if (m && (M.macros_[m] || M.macro1s_[m]))
                    return s; // e.g. \it or \sc
                var t = '&'+(e || m)+';', res = $('<span>'+t+'</span>').text();
                return res != t ? res : ents_[e || m] || s;
            });



    //var methodologyRuMath = 'R_i и R_j, длинною соответственно $l_i$ и $l_j$. Пусть дан $u, u \\in R_i$ $r_i(u)$ равен его номеру $n_i(u)$ в этом списке. Пусть $r_j(u)$ - ранг объекта $u$ в списке $R_j$. Тогда, если $u \\in R_j$, то $r_j(u) = n_j(u)$, где $n_j(u)$ - номер объекта $u$ в списке $R_j$, иначе $r_j(u) = l_j + 1$. То есть если $u$ принадлежит списку $R_j$, то ранг $u$ в $R_j$ равен номеру $u$ в этом списке, в противоположном случае ранг $u$ в $R_j$ равен $l_j + 1$ - на единицу больше длины списка $R_j$. Далее, совокупный ранг $r_k$ объекта $u_k$ вычисляется следующим образом: $r_k = \\sum\\limits_{j = 1}^{N}r_j(u_k)$,  где $r_j(u_k)$ - ранг $u_k$ в списке $R_j$, $N$ - число ранжированных списков ($j = 1,2,3\\ldots N$ - номера списков), то есть он просто равен сумме всех рангов для всех списков рангов. Другие, более изощрённые подходы (без приписывания весовых коэффициентов каждому из рангов) подобные использованным в работе [3] существенного результата бы не дали — конечная ранжировка в интегрированном рейтинге не изменилась бы.';

    var methodologyRuMath = 'R_i и R_j, длинною соответственно l_i и l_j. Пусть дан u, u \\in R_i r_i(u) равен его номеру n_i(u) в этом списке. Пусть r_j(u) - ранг объекта u в списке R_j. Тогда, если $u \\in R_j$, то $r_j(u) = n_j(u)$, где $n_j(u)$ - номер объекта $u$ в списке $R_j$, иначе $r_j(u) = l_j + 1$. То есть если $u$ принадлежит списку $R_j$, то ранг $u$ в $R_j$ равен номеру $u$ в этом списке, в противоположном случае ранг $u$ в $R_j$ равен $l_j + 1$ - на единицу больше длины списка $R_j$. Далее, совокупный ранг $r_k$ объекта $u_k$ вычисляется следующим образом: $r_k = \\sum\\limits_{j = 1}^{N}r_j(u_k)$,  где $r_j(u_k)$ - ранг $u_k$ в списке $R_j$, $N$ - число ранжированных списков ($j = 1,2,3\\ldots N$ - номера списков), то есть он просто равен сумме всех рангов для всех списков рангов. Другие, более изощрённые подходы (без приписывания весовых коэффициентов каждому из рангов) подобные использованным в работе [3] существенного результата бы не дали — конечная ранжировка в интегрированном рейтинге не изменилась бы.';

    var methodologyRu = '$R_i$ и $R_j$, длинною соответственно $l_i$ и $l_j$. Пусть дан $u, u \\in R_i$ $r_i(u)$ равен его номеру $n_i(u)$ в этом списке. Пусть $r_j(u)$ - ранг объекта $u$ в списке $R_j$. Тогда, если $u \\in R_j$, то $r_j(u) = n_j(u)$, где $n_j(u)$ - номер объекта $u$ в списке $R_j$, иначе $r_j(u) = l_j + 1$. То есть если $u$ принадлежит списку $R_j$, то ранг $u$ в $R_j$ равен номеру $u$ в этом списке, в противоположном случае ранг $u$ в $R_j$ равен $l_j + 1$ - на единицу больше длины списка $R_j$. Далее, совокупный ранг $r_k$ объекта $u_k$ вычисляется следующим образом: $$r_k = ∑↙{i=1}↖N r_j(u_k)$$,  где $r_j(u_k)$ - ранг $u_k$ в списке $R_j$, $N$ - число ранжированных списков $($$j = 1,2,3…N$ - номера списков$)$, то есть он просто равен сумме всех рангов для всех списков рангов. Другие, более изощрённые подходы (без приписывания весовых коэффициентов каждому из рангов) подобные использованным в работе [3] существенного результата бы не дали — конечная ранжировка в интегрированном рейтинге не изменилась бы.';
    methodologyRuMath = methodologyRuMath.replace(/&([-#.\w]+);|\\([a-z]+)(?: |(?=[^a-z]))/ig,
            function(s, e, m) {
                if (m && (M.macros_[m] || M.macro1s_[m]))
                    return s; // e.g. \it or \sc
                var t = '&'+(e || m)+';', res = $('<span>'+t+'</span>').text();
                return res != t ? res : ents_[e || m] || s;
            });


    $scope.changeLanguage = function() {
        var mathDiv = angular.element(document.getElementById('methodolgyMath'));
        mathDiv.html('');
        if ($scope.langSelect.selectedLang.id == 0) {
            $scope.langValues = langEnValues;
            $scope.methodology = methodologyEn;
            //M.parseMath(document.body);
            //mathDiv.append(translateToMath);
            //mathDiv.append(M.sToMathE(methodologyEnMath));
            mathDiv.html(methodologyEn);
            //var mathDiv = angular.element(document.getElementById('methodolgyMath'));
            //M.parseMath(mathDiv);
        }
        else if ($scope.langSelect.selectedLang.id == 1) {
            $scope.langValues = langRuValues;
            $scope.methodology = methodologyRu;
            //M.parseMath(document.body);
            //mathDiv.append(M.sToMathE(methodologyRuMath));
            mathDiv.html(methodologyRu);
            //var mathDiv = angular.element(document.getElementById('methodolgyMath'));
            //M.parseMath(mathDiv);

        }
        //MathJax.Hub.Queue(['Typeset', MathJax.Hub, 'methodolgyMath']);
        //M.parseMath('methodolgyMath');
        //var mathDiv = angular.element(document.getElementById('methodolgyMath'));
        //M.parseMath(mathDiv);

        //mathDiv.html("ABC");
        //mathDiv.append('<strong> ABC </strong>');
        //mathDiv.append(translateToMath);
        M.parseMath(document.body);
    };
    

    $scope.changeLanguage();

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
