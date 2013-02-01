
function createQueueObject()
{
    $.ajax({
        type: "POST",
        url: "/update/create/",
        dataType: "html",
        cache: false,
        headers: {
            "Content-type" : "application/x-www-form-urlencoded",
            "X-CSRFToken" : $.cookie('csrftoken')
        },
        data: JSON.stringify({
            "ps" : $('input#dpq-add-queue-ps').val(),
            "description" : $('input#dpq-add-queue-description').val(),
            "branch" : $('select#dpq-add-queue-branch').val(),
            "devA" : $('input#dpq-add-queue-devA').val(),
            "devB" : $('input#dpq-add-queue-devB').val(),
            "tester" : $('input#dpq-add-queue-tester').val()
        })
    }).done(function() {
        refreshQueue();
        $('div#dpq-add-queue button.close').click();
    });
}

function modifyQueueObject()
{
    $.ajax({
        type: "POST",
        url: "/update/modify/",
        dataType: "html",
        cache: false,
        headers: {
            "Content-type" : "application/x-www-form-urlencoded",
            "X-CSRFToken" : $.cookie('csrftoken')
        },
        data: JSON.stringify({
            "ps" : $('input#dpq-modify-queue-ps').val(),
            "description" : $('input#dpq-modify-queue-description').val(),
            "branch" : $('select#dpq-modify-queue-branch').val(),
            "devA" : $('input#dpq-modify-queue-devA').val(),
            "devB" : $('input#dpq-modify-queue-devB').val(),
            "tester" : $('input#dpq-modify-queue-tester').val(),
            "status" : $('select#dpq-modify-queue-status').val(),
            "index" : $('input#dpq-modify-queue-index').val(),
            "owner" : $('input#dpq-modify-queue-owner').val(),
            "id" : $('input#dpq-modify-queue-id').val()
        })
    }).done(function() {
        refreshQueue();
        $('div#dpq-modify-queue button.close').click();
    });
}

function refreshQueue()
{
    if($('div#queue-table').length != 0) {
      $.ajax({
          type: "GET",
          url: "/update/refresh/" + $("div.dpq-queue-tabs > ul > li.active").attr("id") + "/",
          dataType: "html",
          cache: false
      }).done(function(data) {
          $('div#queue-table').html(data);
          $('div#dpq-refresh-alert').hide("slow");
      }).fail(function() {
          $('div#dpq-refresh-alert').show("slow");
      });
    }
}

function fetchQueueObject(queue_id)
{
    $.ajax({
        type: "POST",
        url: "/update/fetch/",
        dataType: "html",
        cache: false,
        headers: {
            "Content-type" : "application/x-www-form-urlencoded",
            "X-CSRFToken" : $.cookie('csrftoken')
        },
        data: JSON.stringify({
            "mode" : "fetch",
            "id" : queue_id
        })
    }).done(function(data) {
        $('div#dpq-modify-queue > div.modal-body').html(data);
    });
}

function fetchLastQueueData()
{
    $.ajax({
        type: "POST",
        url: "/update/fetch/",
        dataType: "html",
        cache: false,
        headers: {
            "Content-type" : "application/x-www-form-urlencoded",
            "X-CSRFToken" : $.cookie('csrftoken')
        },
        data: JSON.stringify({
            "mode" : "last"
        })
    }).done(function(data) {
        $('div#dpq-add-queue > div.modal-body').html(data);
    });
}

function clearModal() {
    $('div#dpq-modify-queue > div.modal-body > form').remove();
}

function timedRefresh() {
    setInterval(function(){refreshQueue()},30000);
}
