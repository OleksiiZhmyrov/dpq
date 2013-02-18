$(document).ready(function () {
    $.ajaxSetup(
        {
			type: "GET",
            dataType: "html",
            cache: false
        });
	
	$('#admin-invalidate-cache').click(function () {
        $.ajax({
			url: "/ajax/admin/invalidate-cache/"
		}).done(function() {
          alert("Cache is invalidated");
		});
    });
});