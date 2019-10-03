$(function () {

    // console.log(window.bell.link_ref);
    $.ajax({
        dataType: 'json',
        url: window.bell.last_event_url,
        success: function (jsondata) {
            if (jsondata.read) {
                $(".bell-status").addClass("not-ring");
                $(".bell-status").removeClass("ring");
            } else {
                $(".bell-status").addClass("ring");
                $(".bell-status").removeClass("not-ring");
            }
        }
    });

});