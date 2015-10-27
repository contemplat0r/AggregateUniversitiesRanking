$.cookie.defaults.path = '/';

$(document).ready(function () {

    $(".popup").click(function () {
        var me = this;
        ShowPopup(me);
        return false;
    });

    $(".mainmenu a, .supermenu a").click(function () {
        $.removeCookie('fromBackButton');
    });


    if (compensatorcontroller.isOldBrowser() && $.cookie('oldbrowsernotified') !== 'true') {
        setTimeout(function () { browsercontroller.notify('<h3>Warning</h3><p>Your web browser is out of date. It may not display all features of this and other websites. We recommend an upgrade to a newer version of your web browser or another web browser. A list of the most popular browsers can be found below. If you choose to continue without upgrading you acknowledge that your experience on this website will be degraded.</p>'); }, 250);
        $.cookie('oldbrowsernotified', 'true');
    }

});

$(document).ajaxStart(function () {
    //alert('start');
});

$(document).ajaxStop(function () {
    //alert('stop');
});


function ShowPopup(element) {

    var url = '';
    
    switch (element.id) {
        case 'cookies':
            url = window.CookiesPopupUrl;
            break;
    }

    if (url.length > 0) {

        if (this.dataRequest) this.dataRequest.abort();

        this.dataRequest = $.ajax({
            url: url,
            success: function (data) {
                ShowShadowbox(data);
            }
        });
    }
    else {
        ShowShadowbox('No information available yet...');
    }

    return false;
}


function ShowShadowbox(data) {
    shadowboxcontroller.shadow({
        modal: true,
        player: 'html',
        content: data,
        width: 600,
        height: 600,
        displayNav: false,
        SBXclass: 'SBXmultimedia'
    });
}
