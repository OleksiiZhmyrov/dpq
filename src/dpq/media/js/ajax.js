$(document).ready(function () {
    $('#dpq-add-queue').find('#btn-save').click(function () {
        if (isValidCreateForm()) {
            disableAddForm();
            createQueueObject();
        }
    });

    $('#dpq-modify-queue').find('#btn-save').click(function () {
        if (isValidModifyForm()) {
            $("#dpq-modify-queue #btn-save").removeClass('btn-primary').attr("disabled", true).html('Working ...');
            $("div#dpq-modify-queue>div.modal-body :input").attr("disabled", true);
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

function disableAddForm() {
    $("#dpq-add-queue #btn-save").removeClass('btn-primary').attr("disabled", true).html('Working ...');
    $("div#dpq-add-queue>div.modal-body :input").attr("disabled", true);
}

function disableAddFormJIRAFetch() {
    $("#dpq-add-queue #btn-save").removeClass('btn-primary').attr("disabled", true);
    $("div#dpq-add-queue>div.modal-body :input").attr("disabled", true);
}

function enableAddFormJIRAFetch() {
    $("#dpq-add-queue #btn-save").addClass('btn-primary').attr("disabled", false).html('Add');
    $("div#dpq-add-queue>div.modal-body :input").attr("disabled", false);
}

function createQueueObject() {
    $.ajax({
        url: "/ajax/create/",
        headers: {
            "Content-type": "application/x-www-form-urlencoded",
            "X-CSRFToken": $.cookie('csrftoken')
        },
        data: JSON.stringify({
            "key": $('input#dpq-add-queue-key').val(),
            "summary": $('input#dpq-add-queue-summary').val(),
            "branch": $('select#dpq-add-queue-branch').val(),
            "team": $('select#dpq-add-queue-team').val(),
            "developer": $('input#dpq-add-queue-developer').val(),
            "tester": $('input#dpq-add-queue-tester').val()
        })
    }).done(function () {
            update_branch_tab($("div.dpq-queue-tabs > ul > li.active").attr("id"));
            $('div#dpq-add-queue button.close').click();
            $("#dpq-add-queue #btn-save").addClass('btn-primary').attr("disabled", false).html('Add');
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
            "key": $('input#dpq-modify-queue-key').val(),
            "summary": $('input#dpq-modify-queue-summary').val(),
            "branch": $('select#dpq-modify-queue-branch').val(),
            "team": $('select#dpq-modify-queue-team').val(),
            "developer": $('input#dpq-modify-queue-developer').val(),
            "tester": $('input#dpq-modify-queue-tester').val(),
            "status": $('select#dpq-modify-queue-status').val(),
            "id": $('input#dpq-modify-queue-id').val()
        })
    }).done(function () {
            update_branch_tab($("div.dpq-queue-tabs > ul > li.active").attr("id"));
            $('div#dpq-modify-queue button.close').click();
            $("#dpq-modify-queue #btn-save").addClass('btn-primary').attr("disabled", false).html('Apply');
        });
}

function update_branch_tab(branch) {
    $.ajax({
        type: "GET",
        url: "/ajax/refresh-branch/" + branch + "/"
    }).done(function (data) {
            $('div#' + branch + '_tab').html(data);
            fetchAndUpdateBranchesStatuses();
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
        $('#dpq-add-queue').find('#dpq-add-queue-jira').click(function () {
            fetchStoryDataFromJIRA();
        });
    });
}


function fetchStoryDataFromJIRA() {
    disableAddFormJIRAFetch();
    $.ajax({
        url: "/ajax/request/jirastory/",
        headers: {
            "Content-type": "application/x-www-form-urlencoded",
            "X-CSRFToken": $.cookie('csrftoken')
        },
        data: JSON.stringify({
            "key": $('input#dpq-add-queue-key').val()
        })
    }).done(function(data) {
        var response = JSON.parse(data);

        $('input#dpq-add-queue-summary').val(response.summary);
        $('input#dpq-add-queue-developer').val(response.assignee);
        $('input#dpq-add-queue-tester').val(response.tester);

        $('span#validation-msg').html('');

    }).fail(function () {
            $('span#validation-msg').html("Could not fetch data from JIRA");
    });
    enableAddFormJIRAFetch();
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
            fetchAndUpdateBranchesStatuses();
            if ($.cookie('key') != data) {
                $.cookie('key', data);
                update_branch_tab($("div.dpq-queue-tabs > ul > li.active").attr("id"));
            }
            $('div#dpq-refresh-alert').hide("slow");
        }).fail(function () {
            $('div#dpq-refresh-alert').show("slow");
        });
}

function fetchAndUpdateBranchesStatuses() {
    $.ajax({
        type: "GET",
        url: "/api/branch/status/"
    }).done(function (data) {
        var response = JSON.parse(data);
        var length = response.length, element = null;
        for (var i = 0; i < length; i++) {
            element = response[i];
            var image = $('li#'+element.branch+' a img');
            if(element.status == true) {
                image.attr('src', '/media/img/build/success_hq.png');
            } else {
                image.attr('src', '/media/img/build/failure_hq.png');
            }
        }
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
    $('a.move-link').replaceWith('<span>&nbsp;&nbsp;</span>');
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


function useJoker(recordId) {
    if(confirm("Are you sure you want to apply Joker?")) {
        $.ajax({
            url: "/api/joker/",
            headers: {
                "Content-type": "application/x-www-form-urlencoded",
                "X-CSRFToken": $.cookie('csrftoken')
            },
            data: JSON.stringify({
                "id": recordId
            })
        }).done(function () {
                update_branch_tab($("div.dpq-queue-tabs > ul > li.active").attr("id"));
            });
    }
}
