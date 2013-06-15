$(document).ready(function () {
    $('#dpq-add-queue').find('#btn-save').click(function () {
        if (isValidCreateForm()) {
            createQueueObject();
        }
    });

    $('#dpq-modify-queue').find('#btn-save').click(function () {
        if (isValidModifyForm()) {
            modifyQueueObject();
        }
    });

    $('a#btn-hero').click(function () {
        $('div#dpq-heroes>div.modal-body').html("<center><img src='/media/img/ajax-loader.gif'/></center>");
        fetchHeroesAndVillainsList();
    });

    $('div#dpq-refresh-alert button.close').click(function () {
        $('div#dpq-refresh-alert').hide("slow");
    });

    $.ajaxSetup(
        {
            type: "POST",
            dataType: "html",
            cache: false
        });
});

function createQueueObject() {
    $.ajax({
        url: "/ajax/create/",
        headers: {
            "Content-type": "application/x-www-form-urlencoded",
            "X-CSRFToken": $.cookie('csrftoken')
        },
        data: JSON.stringify({
            "ps": $('input#dpq-add-queue-ps').val(),
            "description": $('input#dpq-add-queue-description').val(),
            "codereview_url": $('input#dpq-add-queue-codereview').val(),
            "team": $('select#dpq-add-queue-team').val(),
            "branch": $('select#dpq-add-queue-branch').val(),
            "devA": $('input#dpq-add-queue-devA').val(),
            "devB": $('input#dpq-add-queue-devB').val(),
            "tester": $('input#dpq-add-queue-tester').val()
        })
    }).done(function () {
            update_branch_tab($("div.dpq-queue-tabs > ul > li.active").attr("id"));
            $('div#dpq-add-queue button.close').click();
        });
}

function modifyQueueObject() {
    $.ajax({
        url: "/ajax/modify/",
        headers: {
            "Content-type": "application/x-www-form-urlencoded",
            "X-CSRFToken": $.cookie('csrftoken')
        },
        data: JSON.stringify({
            "ps": $('input#dpq-modify-queue-ps').val(),
            "description": $('input#dpq-modify-queue-description').val(),
            "codereview_url": $('input#dpq-modify-queue-codereview').val(),
            "branch": $('select#dpq-modify-queue-branch').val(),
            "team": $('select#dpq-modify-queue-team').val(),
            "devA": $('input#dpq-modify-queue-devA').val(),
            "devB": $('input#dpq-modify-queue-devB').val(),
            "tester": $('input#dpq-modify-queue-tester').val(),
            "status": $('select#dpq-modify-queue-status').val(),
            "index": $('input#dpq-modify-queue-index').val(),
            "owner": $('input#dpq-modify-queue-owner').val(),
            "id": $('input#dpq-modify-queue-id').val()
        })
    }).done(function () {
            update_branch_tab($("div.dpq-queue-tabs > ul > li.active").attr("id"));
            $('div#dpq-modify-queue button.close').click();
        });
}

function update_branch_tab(branch) {
    $.ajax({
        type: "GET",
        url: "/ajax/refresh-branch/" + branch + "/"
    }).done(function (data) {
            $('div#' + branch + '_tab').html(data);
        }).fail(function () {
            $('div#dpq-refresh-alert').show("slow");
        })
}

function fetchPushDetails(queue_id) {
    $('div#dpq-detailed-info').html('<center><img src="/media/img/ajax-loader.gif" /></center>');
    $.ajax({
        type: "GET",
        url: "/ajax/request/info/" + queue_id + "/",
        headers: {
            "Content-type": "application/x-www-form-urlencoded"
        }
    }).done(function (data) {
            $('div#dpq-detailed-info').html(data);
        });
}

function fetchQueueObject(queue_id) {
    $.ajax({
        url: "/ajax/request/fetch/",
        headers: {
            "Content-type": "application/x-www-form-urlencoded",
            "X-CSRFToken": $.cookie('csrftoken')
        },
        data: JSON.stringify({
            "mode": "fetch",
            "id": queue_id
        })
    }).done(function (data) {
            $('div#dpq-modify-queue > div.modal-body').html(data);
        });
}

function fetchLastQueueData() {
    $.ajax({
        url: "/ajax/request/fetch/",
        headers: {
            "Content-type": "application/x-www-form-urlencoded",
            "X-CSRFToken": $.cookie('csrftoken')
        },
        data: JSON.stringify({
            "mode": "last"
        })
    }).done(function (data) {
            $('div#dpq-add-queue > div.modal-body').html(data);
        });
}

function clearModal() {
    $('div#dpq-modify-queue > div.modal-body > form').remove();
}

function timedRefresh() {
    var tick = 9;
    setInterval(function() {
        $('#timer-ajax-loader').hide();
        $('#timer').html("0:0" + tick);
        if(tick == 0) {
            $('#timer-ajax-loader').show();
            $('#timer').html("&nbsp;updating...");
            updateTab();
            tick = 10;
        }
        tick--;
    }, 1000);
}

function updateTab() {
    $.ajax({
        type: "GET",
        url: "/ajax/request/key/"
    }).done(function (data) {
            if ($.cookie('key') != data) {
                $.cookie('key', data);
                update_branch_tab($("div.dpq-queue-tabs > ul > li.active").attr("id"));
            }
            $('div#dpq-refresh-alert').hide("slow");
        }).fail(function () {
            $('div#dpq-refresh-alert').show("slow");
        });
}


function fetchSuperusersList() {
    $.ajax({
        type: "GET",
        url: "/ajax/request/superusers/"
    }).done(function (data) {
            $('div#dpq-superusers-list').html(data);
        }).fail(function () {
            $('div#dpq-superusers-list').html('<center>Request failed.</center>');
        });
}

function moveRecord(queue_id, direction) {
    $.ajax({
        url: "/ajax/move/",
        headers: {
            "Content-type": "application/x-www-form-urlencoded",
            "X-CSRFToken": $.cookie('csrftoken')
        },
        data: JSON.stringify({
            "mode": direction,
            "id": queue_id
        })
    }).done(function () {
            update_branch_tab($("div.dpq-queue-tabs > ul > li.active").attr("id"));
        });
}


function fetchHeroesAndVillainsList() {
    $.ajax({
        type: "GET",
        url: "/ajax/request/heroes/"
    }).done(function (data) {
            $('div#dpq-heroes>div.modal-body').html(data);
        }).fail(function () {
            $('div#dpq-heroes>div.modal-body').html('<center>Request failed.</center>');
        });
}