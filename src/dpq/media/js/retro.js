$(document).ready(function () {
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