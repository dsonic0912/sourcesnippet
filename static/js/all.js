$(document).ready(function() {
	$("#notifyModal").modal('hide');

	$("#btnNotify").click(function() {
		var user_id = $("#g_user_id").val();
		if (user_id <= 0) {
			window.location.href = "/signin";
		}
	});
});