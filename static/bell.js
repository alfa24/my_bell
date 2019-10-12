$(function () {

    $.dynatableSetup({
        // your global default options here
        features: {
            paginate: false,
            sort: false,
            pushState: true,
            search: false,
            recordCount: false,
            perPageSelect: true
        },
    });
    var dt = $('.events-table').dynatable({
        dataset: {
            records: []
        }
    }).data('dynatable');


    // проверить последнее событие
    var check_last_event = function () {
        $.ajax({
            dataType: 'json',
            url: window.bell.last_event_url,
            success: function (jsondata) {
                if (jsondata.read || jsondata.read === undefined) {
                    $(".bell-status audio").trigger("pause");
                    $(".bell-status__text").text("Ждем события....");
                    $(".bell-status").addClass("not-ring");
                    $(".bell-status").removeClass("ring");
                } else {
                    $(".bell-status__text").text(jsondata.text);
                    $(".bell-status").addClass("ring");
                    $(".bell-status").removeClass("not-ring");
                    $(".bell-status audio").trigger("play");
                }
            }
        });
    };

    // обновить список последних событий
    var update_latest_events = function () {
        $.ajax({
            dataType: 'json',
            url: window.bell.latest_events_url,
            success: function (jsondata) {
                dt.settings.dataset.originalRecords = jsondata;
                dt.process();
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
        update_latest_events();
        timerId = setTimeout(tick, 2000);
    }, 2000);
});