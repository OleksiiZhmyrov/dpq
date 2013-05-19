$(document).ready(function () {
    $.ajaxSetup(
        {
            type: "POST",
            dataType: "html",
            cache: false
        });

    $('input#dpq-search-searchstring').on('keyup', function(){
        var searchStringLengt = $('input#dpq-search-searchstring').val().length;
        console.log("Search string length is " + searchStringLengt);
        if(searchStringLengt < 3) {
            $('div#dpq-search-searchresults').html('');
        }
        if(searchStringLengt >= 3){
            $('div#dpq-search-searchresults').html('<img src="/media/img/ajax-loader.gif"/>');
            requestSearchResults();
        }
    });

});

function requestSearchResults() {
    $.ajax({
        url: "/ajax/search/",
        headers: {
            "Content-type": "application/x-www-form-urlencoded",
            "X-CSRFToken": $.cookie('csrftoken')
        },
        data: JSON.stringify({
            "search_string": $('input#dpq-search-searchstring').val()
        })
    }).done(function(data) {
            updateSearchResults(data);
        });
}

function updateSearchResults(data) {
    $('div#dpq-search-searchresults').html(data);
}