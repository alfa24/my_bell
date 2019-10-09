$(function () {

    // проверить последнее событие
    var check_last_event = function () {
        $.ajax({
            dataType: 'json',
            url: window.bell.last_event_url,
            success: function (jsondata) {
                if (jsondata.read || jsondata.read === undefined) {
                    $(".bell-status__text").text("Ждем события....");
                    $(".bell-status").addClass("not-ring");
                    $(".bell-status").removeClass("ring");
                } else {
                    $(".bell-status__text").text(jsondata.text);
                    $(".bell-status").addClass("ring");
                    $(".bell-status").removeClass("not-ring");
                }
            }
        });
    };

    //отметить все события как прочитанные
    var read_all_events = function (e) {
        $.ajax({
            dataType: 'json',
            type: "POST",
            url: window.bell.read_events_url,
            success: function (jsondata) {
                check_last_event();
            }
        });
    };

    $(".bell-status__read").bind("click", read_all_events);

    //бесконечная проверка событий
    var timerId = setTimeout(function tick() {
        check_last_event();
        timerId = setTimeout(tick, 2000);
    }, 2000);


});