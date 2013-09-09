$(document).ready(function() {
	$("#newProjectError").hide();
	var host_url = 'http://' + window.location.host;
	// initialisation
	editAreaLoader.init({
		id: "newSnippetSnippet"	// id of the textarea to transform		
		,start_highlight: true	// if start with highlight
		//,allow_resize: "both"
		,allow_toggle: false
		,word_wrap: false
		,language: "en"
		//,syntax: "php"
		,replace_tab_by_spaces: 2
		,is_editable: true
		,font_size: 10
		,toolbar: "search, go_to_line, fullscreen, |, undo, redo, |, select_font, |, syntax_selection, |, change_smooth_selection, highlight, reset_highlight"
		,syntax_selection_allow: "css,html,js,php,python,vb,xml,c,cpp,sql,basic,pas,brainfuck"
	});

	$("#btnNewProject").click(function() {
		var project_name = $("#newSnippetProjectName").val();
		var user_id = $("#newProjectUserId").val();
		var params = {
			'project_name': project_name,
			'user_id': user_id
		}
		$.post(host_url + '/new_project', params, function(data) {
			if (data.status) {
				window.location.href = "/new_snippet";
			} else {
				var error_msg = '<strong>Error!</strong> ';
				switch (data.error_code) {
					case 1:
						error_msg += 'Permission Denied...';
						break;
					case 2:
						error_msg += 'Duplicate Name....';
						break;
					case 3:
						error_msg += "Project Name can't be empty";
				}
				$("#newProjectError").html(error_msg);
				$("#newProjectError").show();
			}
		}, 'json');
	});

	$('#newProjectModel').on('hidden', function () {
		$("#newProjectError").hide();
	});

	$("#newSnippetCancel").click(function() {
		window.location.href = '/mysnippets';
	});

	var txtPublic = $("#txtNewSnippetPublic").val();
	var txtImprove = $("#txtNewSnippetImprove").val();

	if (txtPublic == 'True') {
		$('#switchPublic').bootstrapSwitch('status');
	} else {
		$('#switchPublic').bootstrapSwitch('setState', false);
	}

	if (txtImprove == 'True') {
		$('#switchImprove').bootstrapSwitch('status');
	} else {
		$('#switchImprove').bootstrapSwitch('setState', false);
	}
});