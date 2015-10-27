// Ajax error handling is done globally in _layout.js



var Ranking2015Form = {

    size_independent:true,
    
    SetCookies : function() {
        $.cookie("field", $("#field").val());
        $.cookie("region", $("#region").val());
        $.cookie("country", $("#country").val());
        $.cookie("performance-dimension", $("#performance-dimension").val());
        $.cookie("ranking-indicator", $("#ranking-indicator").val());
        $.cookie("number-of-publications", $("#number-of-publications").val());
        $.cookie("period_id", $("#period_id").val());
        $.cookie("size-independent", Ranking2015Form.size_independent);
        $.cookie("fractional_counting", $("#fractional_counting").val());
        $.cookie("show-stability-intervals", $("#show-stability-intervals").val());
    },

    GetCookies : function() {
        $("#field").val($.cookie("field"));
        $("#region").val($.cookie("region"));
        $("#country").val($.cookie("country"));
        $("#performance-dimension").val($.cookie("performance-dimension"));
        $("#ranking-indicator").val($.cookie("ranking-indicator"));
        $("#number-of-publications").val($.cookie("number-of-publications"));
        $("#period_id").val($.cookie("period_id"));
        Ranking2015Form.size_independent = $.cookie("size-independent") === "true" ? true : false;
        $("#fractional_counting").val($.cookie("fractional_counting"));
        $("#show-stability-intervals").val($.cookie("show-stability-intervals"));

        if (Ranking2015Form.size_independent) {
            Ranking2015Form.ToggleSizeDependentButton("size-independent");
        } else {
            Ranking2015Form.ToggleSizeDependentButton("size-dependent");
        }

    },

    ClearCookies : function() {
        $.removeCookie("field");
        $.removeCookie("region");
        $.removeCookie("country");
        $.removeCookie("performance-dimension");
        $.removeCookie("ranking-indicator");
        $.removeCookie("number-of-publications");
        $.removeCookie("period_id");
        $.removeCookie("size-independent");
        $.removeCookie("fractional_counting");
        $.removeCookie("show-stability-intervals");
        $.removeCookie("posY");
        $.removeCookie("showAdvancedParameters");
    },

    SavePosition : function() {
        $.cookie("posY", $(window).scrollTop());
    },

    SetPosition: function () {
        var y = ($.cookie("posY") == null) ? 0 : $.cookie("posY");
        window.scroll(0, y);
        $.removeCookie("posY");
    },

    ToggleSizeDependentButton: function (state) {
        $(".togglebutton").removeClass("toggle-on").removeClass("toggle-off");
        if (state === "size-dependent") {
            $("#size-dependent-button").addClass("toggle-on");
            $("#size-independent-button").addClass("toggle-off");
            if (Ranking2015Form.size_independent == true) {
                Ranking2015Form.size_independent = false;
            }
            $("#show-stability-intervals-container").hide();
            $("#number-of-publications-container").hide();
        } else {
            $("#size-dependent-button").addClass("toggle-off");
            $("#size-independent-button").addClass("toggle-on");
            if (Ranking2015Form.size_independent == false) {
                Ranking2015Form.size_independent = true;
            }
            $("#show-stability-intervals-container").show();
            $("#number-of-publications-container").show();
        }

    }


};

$(window).on("beforeunload", function () {
    Ranking2015Form.SetCookies();
    Ranking2015Form.SavePosition();
});

function ChangeCountriesAndShowRanking() {

    // This function handles a change in region from the select form. It will fetch the corresponding countries from the server.
    // The format of the response is a HTML Select which can be inserted in the DOM.

    if (this.dataRequest) this.dataRequest.abort();

    this.dataRequest = $.ajax({
        url: window.Countries2015Url,
        type: "POST",
        data: {
            region: $("#region").val()
        },
        success: function (data) {
            var countrySelectionDiv = $("#country-selection")[0];
            if (countrySelectionDiv && data.length > 0) {
                countrySelectionDiv.innerHTML = data;
                $("#country").change(ShowRanking);
                ShowRanking();
            }
        }
    });

}


function ChangeRankingIndicatorSelection(currentIndex) {

    // Change the content of the ranking indicator dropdown based on the current form values.
    // If currentIndex not is null set the index of the new dropdown to the currentIndex otherwise to the default selected.
    // Finally show the ranking based on the new selected ranking indicator.

    var indexIsObject = (typeof (currentIndex) === "object");

    if (this.dataRequest) this.dataRequest.abort();

    this.dataRequest = $.ajax({
        url: window.Ranking2015IndicatorsUrl,
        type: "POST",
        data: {
            performanceDimension: $("#performance-dimension").val(),
            sizeIndependent: Ranking2015Form.size_independent || Ranking2015Form.size_independent === "true",
            period: $("#period_id option:selected").text()
},
        success: function (data) {

            var rankingIndicatorSelectionDiv = $("#ranking-indicator-selection")[0];

            if (rankingIndicatorSelectionDiv && data.length > 0) {
                rankingIndicatorSelectionDiv.innerHTML = data;
                if (!indexIsObject) {
                    $("#ranking-indicator")[0].selectedIndex = currentIndex;
                }
                $("#ranking-indicator").change(ShowRanking);

                ShowRanking();
            }
        }
    });
}


var fetchTimer;
function ShowRanking() {
    if (fetchTimer) clearTimeout(fetchTimer); //reset timer
    fetchTimer = setTimeout(function () { GetRanking(); }, 250);
}


function GetRanking() {

    if ($("#performance-dimension").val() === "Impact") {
        $("#fractional_counting_label").show();
    } else {
        $("#fractional_counting_label").hide();
    }


    var resultDiv = $("#ranking-search-result");

    if (resultDiv) {
        // Show waiting message
        resultDiv[0].innerHTML = "<div class=\"tablewrapper\"><div class=\"table\"><table class=\"pagedtable ranking\" style=\"width:100%;\" data-table=\"non-paged\"><thead><tr><th><img src=\"../content/images/ajax-loader.gif\" style=\"vertical-align: middle; margin-right: 10px;\"/>Loading...</th></tr></thead></table></div></div>";

        if (this.dataRequest) this.dataRequest.abort();

        // Get the ranking table with the current form values.
        this.dataRequest = $.ajax({
            url: window.Ranking2015Url,
            type: "POST",
            data: {
                field_id: $("#field").val(),
                continent_code: $("#region").val(),
                country_code: $("#country").val(),
                performance_dimension: $("#performance-dimension").val() == "Impact" ? false : true,
                ranking_indicator: $("#ranking-indicator").val(),
                stability_interval: $("#show-stability-intervals").is(":checked"),
                size_independent: Ranking2015Form.size_independent,
                fractional_counting: $("#fractional_counting").is(":checked"),
                core_pub_only: $("#core_pub_only").is(":checked"),
                number_of_publications: $("#number-of-publications").val(),
                period_id: $("#period_id").val(),
                period_text: $("#period_id option:selected").text()
            },
            success: function (data) {
                // Show the ranking table
                if (data.length > 0) {
                    // Bug in IE9 met grote tabellen
                    data = data.replace(/>\s+(?=<\/?(t|c)[hardfob])/gm, ">");
                    resultDiv[0].innerHTML = data;
                    resultDiv.selectivizr();
                }

                // Adjust the UI to the new ranking table
                $("body").tooltips();
                windowcontroller.resize();

                if ($.cookie("fromBackButton") === "true") Ranking2015Form.SetPosition();
                $.cookie("fromBackButton", "false");
            }
        });
    }
}

$(document).ready(function () {

    $.cookie("refresh-university", "");

    if ($.cookie("fromBackButton") && $.cookie("fromBackButton") === "true") {
        Ranking2015Form.GetCookies();
    } else {
        Ranking2015Form.ClearCookies();
        if ($("#size-independent-button").hasClass("toggle-on")) {
            Ranking2015Form.ToggleSizeDependentButton("size-independent");
        } else
        {
            Ranking2015Form.ToggleSizeDependentButton("size-dependent");
        }
    }

    // Prevent all tooltips to be clicked.
    $(".form-tooltip").click(function () { return false; });

    //Setup the event handlers for the elements on the select form.
    $("#field").change(ShowRanking);
    $("#region").change(ChangeCountriesAndShowRanking);
    $("#country").change(ShowRanking);
    $("#performance-dimension").change(ChangeRankingIndicatorSelection);
    $("#ranking-indicator").change(ShowRanking);
    $("#core_pub_only").change(ShowRanking);
    $("#fractional_counting").change(ShowRanking);
    $("#show-stability-intervals").change(ShowRanking);
    $("#number-of-publications").change(ShowRanking);
    //$("#period_id").change(ShowRanking);

    $("#period_id").change(function () {
        ChangeRankingIndicatorSelection($("#ranking-indicator")[0].selectedIndex);
        ShowRanking();
    });

    $("#size-dependent-button").click(function () {
        Ranking2015Form.ToggleSizeDependentButton("size-dependent");
        ChangeRankingIndicatorSelection($("#ranking-indicator")[0].selectedIndex);
    });
    $("#size-independent-button").click(function() {
        Ranking2015Form.ToggleSizeDependentButton("size-independent");
        ChangeRankingIndicatorSelection($("#ranking-indicator")[0].selectedIndex);
    });


    // At startup of the page initialy show the ranking.
    ChangeRankingIndicatorSelection($("#ranking-indicator")[0].selectedIndex);
});

