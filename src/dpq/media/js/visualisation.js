$(document).ready(function () {

    drawAveragePushDuration();
    drawPushDailyCount();

    $.ajaxSetup(
        {
            type: 'GET',
            dataType: 'json',
            cache: false,
            async: false
        });
});

function drawAveragePushDuration() {

    function drawVisualization() {
        var json_data = $.ajax({
            url: '/ajax/request/visualisation/average/'
        }).responseText;

        var parsed_data = JSON.parse(json_data);

        var data = google.visualization.arrayToDataTable(parsed_data);
        var ac = new google.visualization.AreaChart(document.getElementById('vis_average'));
        ac.draw(data, {
            legend: 'none',
            title: 'Average push duration for past period',
            isStacked: true,
            width: 1200,
            height: 400,
            vAxis: {title: "Time, mins"},
            hAxis: {title: "Date"}
        });
    }

    google.setOnLoadCallback(drawVisualization);
}

function drawPushDailyCount() {

    function drawVisualization() {
        var json_data = $.ajax({
            url: '/ajax/request/visualisation/daily/'
        }).responseText;

        var parsed_data = JSON.parse(json_data);

        var data = google.visualization.arrayToDataTable(parsed_data);
        var ac = new google.visualization.AreaChart(document.getElementById('vis_daily'));
        ac.draw(data, {
            legend: 'none',
            title: 'Push count for past period',
            isStacked: true,
            width: 1200,
            height: 400,
            vAxis: {title: "Push count"},
            hAxis: {title: "Date"}
        });
    }

    google.setOnLoadCallback(drawVisualization);
}

function drawVisualisation(branch) {
    drawBranchDuration(branch);
    drawBranchPending(branch);
}

function drawBranchDuration(branch) {

    var json_data = $.ajax({
        url: '/ajax/request/visualisation/branch/' + branch + '/duration/'
    }).responseText;

    var parsed_data = JSON.parse(json_data);
    var data = google.visualization.arrayToDataTable(parsed_data);

    var options = {
        title: 'Push duration',
        legend: 'none',
        vAxis: {title: 'Time, mins'},
        hAxis: {title: 'Developer'}
    };

    var chart = new google.visualization.ColumnChart(document.getElementById('duration_branch_' + branch));
    chart.draw(data, options);
}

function drawBranchPending(branch) {

    var json_data = $.ajax({
        url: '/ajax/request/visualisation/branch/' + branch + '/pending/'
    }).responseText;

    var parsed_data = JSON.parse(json_data);
    var data = google.visualization.arrayToDataTable(parsed_data);

    var options = {
        title: 'Pending time',
        legend: 'none',
        vAxis: {title: 'Time, mins'},
        hAxis: {title: 'Developer'}
    };

    var chart = new google.visualization.ColumnChart(document.getElementById('pending_branch_' + branch));
    chart.draw(data, options);
}