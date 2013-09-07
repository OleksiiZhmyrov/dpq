$(document).ready(function () {
    $.ajaxSetup(
        {
            type: "POST",
            dataType: "html",
            cache: false
        });
    $('#dpq-cards-search').find('#search-btn').click(function () {
        disableButton();
        queryCards();
    });
    $('#clear-btn').click(function () {
        $('#dpq-print-cards').find('input#print-data').val('');
        disablePrintButton();
        $('tbody#results').html('');
    });

});

function queryCards() {
    $.ajax({
        url: "/ajax/request/jirastory/",
        headers: {
            "Content-type": "application/x-www-form-urlencoded",
            "X-CSRFToken": $.cookie('csrftoken')
        },
        data: JSON.stringify({
            "key": $('input#dpq-cards-key').val()
        })
    }).done(function(data) {
        var response = JSON.parse(data);
        var content = $('tbody#results').html();
        var newStory = '<tr>><td>'+response.key+'</td><td>'+response.summary+'</td><td>'+response.assignee
            +'</td><td>'+response.tester+'</td><td>'+response.reporter+'</td><td>'+response.sp+'</td></tr>';

        $('tbody#results').html(content+newStory);
        appendStoryToRequest(response.key);
        enablePrintButton();
        enableButton();
        $('span#validation-msg').html('');

    }).fail(function () {
            $('span#validation-msg').html("Could not fetch data from JIRA");
            enableButton();
    });
}

function disableButton() {
    $('#dpq-cards-search').find('#search-btn').addClass('disabled');
}

function enableButton() {
    $('#dpq-cards-search').find('#search-btn').removeClass('disabled');
}

function enablePrintButton() {
    if ($('#dpq-print-cards').find('input#print-data').value != '') {
        $('#dpq-print-cards').find('#print-btn').removeClass('disabled');
        $('#dpq-print-cards').find('#print-btn').removeAttr('disabled');
    }
}

function disablePrintButton() {
    $('#dpq-print-cards').find('#print-btn').addClass('disabled');
    $('#dpq-print-cards').find('#print-btn').attr('disabled', 'disabled');
}

function appendStoryToRequest(key) {
    var requestData = $('#dpq-print-cards').find('input#print-data');
    requestData.val(requestData.val() + key + ',');
    $('input#dpq-cards-key').val('');
}