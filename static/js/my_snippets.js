$(document).ready(function() {
	$(".delete-snippet").click(function() {
		var url = $(this).attr('url');

		$("#mysnippetDeleteModal").modal('show');

		$("#deleteSnippetYes").click(function() {
			window.location.href = url;
		});
	});
});