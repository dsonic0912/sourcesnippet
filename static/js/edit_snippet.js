$(document).ready(function() {
	var cat_name = $("#cat_name").val();

	if (cat_name == 'Untitled') {
		cat_name = 'python';
	}

	// initialisation
	editAreaLoader.init({
		id: "editSnippetSnippet"	// id of the textarea to transform		
		,start_highlight: true	// if start with highlight
		//,allow_resize: "both"
		,allow_toggle: false
		,word_wrap: false
		,language: "en"
		,syntax: cat_name
		,replace_tab_by_spaces: 2
		,is_editable: true
		,font_size: 10
		,toolbar: "search, go_to_line, fullscreen, |, undo, redo, |, select_font, |, syntax_selection, |, change_smooth_selection, highlight, reset_highlight"
		,syntax_selection_allow: "css,html,js,php,python,vb,xml,c,cpp,sql,basic,pas,brainfuck"
	});

	var txtPublic = $("#txtEditSnippetPublic").val();
	var txtImprove = $("#txtEditSnippetImprove").val();

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

	$("#editSnippetCancel").click(function() {
		window.location.href = '/mysnippets';
	});
});