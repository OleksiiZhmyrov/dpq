$(document).ready(function () {
    $.ajaxSetup(
        {
            type: "POST",
            dataType: "html",
            cache: false
        });

    $('input#dpq-search-searchstring').on('keyup', function(){
        var searchStringLengt = $('input#dpq-search-searchstring').val().length;

        if(searchStringLengt < 3) {
            $('div#dpq-search-searchresults').html('');
        }
        if(searchStringLengt >= 3){
            $('div#dpq-search-searchresults').html('<img src="/media/img/ajax-loader.gif"/>');
            requestSearchResults();
        }
    });

    $.fn.highlight = function(what,spanClass) {
    return this.each(function(){
        var container = this,
            content = container.innerHTML,
            pattern = new RegExp('(>[^<.]*)(' + what + ')([^<.]*)','gi'),
            replaceWith = '$1<span ' + ( spanClass ? 'class="' + spanClass + '"' : '' ) + '">$2</span>$3',
            highlighted = content.replace(pattern,replaceWith);
        container.innerHTML = highlighted;
    });
}

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

    var searchString = $('input#dpq-search-searchstring').val();
    $('div#dpq-search-searchresults').highlight(searchString, 'highlight')
}
