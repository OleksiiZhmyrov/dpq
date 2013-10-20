$(document).ready(function () {
    $('div#retro-add-popup').find('#btn-save').click(function () {
        if (retroIsValidAddForm()) {
            retroDisableAddForm();
            addSticker();
        }
    });
    $.ajaxSetup(
        {
            type: "POST",
            dataType: "html",
            cache: false
    });
    update_board();
});

function update_board() {
    var sprint = $('input#retro-sprint').val();
    var team = $('input#retro-team').val();
    $.ajax({
        type: "GET",
        url: "/api/retro/" + sprint + "/" + team + "/"
    }).done(function (data) {
            $('div#retro-board-tables').html(data);
            $('div#retro-refresh-alert').hide("slow");
        }).fail(function () {
            $('div#retro-refresh-alert').show("slow");
        })
}

function retroTimedRefresh() {
    var tick = 29;
    setInterval(function() {
        $('#timer-ajax-loader').hide();
        var tickPretty = tick < 10 ? "0" + tick : tick;
        $('#timer').html("0:" + tickPretty);
        if(tick == 0) {
            $('#timer-ajax-loader').show();
            $('#timer').html("&nbsp;updating...");
            update_board();
            tick = 30;
        }
        tick--;
    }, 1000);
}

function clearAddPopup() {
    retroEnableAddForm();
    $('textarea#retro-sticker-summary').val("");
}

function addSticker() {
    $.ajax({
        url: "/api/retro/sticker/add/",
        headers: {
            "Content-type": "application/x-www-form-urlencoded",
            "X-CSRFToken": $.cookie('csrftoken')
        },
        data: JSON.stringify({
            "summary": $('textarea#retro-sticker-summary').val(),
            "sprint": $('input#retro-sprint').val(),
            "team": $('input#retro-team').val(),
            "type": $('select#retro-add-sticker-type').val()
        })
    }).done(function () {
            update_board();
            $('div#retro-add-popup button.close').click();
            $("#retro-add-popup #btn-save").addClass('btn-primary').attr("disabled", false).html('Add');
        });
}

function retroDisableAddForm() {
    $("#retro-add-popup #btn-save").removeClass('btn-primary').attr("disabled", true).html('Working ...');
    $("div#retro-add-popup textarea").attr("disabled", true);
}

function retroEnableAddForm() {
    $("#retro-add-popup #btn-save").addClass('btn-primary').attr("disabled", false).html('Add');
    $("div#retro-add-popup textarea").attr("disabled", false);
}