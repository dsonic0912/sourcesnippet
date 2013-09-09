$(document).ready(function() {
	var improve = $("#publicSnippetImprove").val();
	var cat_name = $("#publicSnippetCatName").val();

	var is_improve = false;

	if (improve == 'True') {
		is_improve = true;
	}

	if (cat_name == 'Untitled') {
		cat_name = 'python'
	}

	// initialisation
	editAreaLoader.init({
		id: "publicSnippetTextArea"	// id of the textarea to transform
		,start_highlight: true	// if start with highlight
		//,allow_resize: "both"
		,allow_toggle: false
		,word_wrap: true
		,language: "en"
		,syntax: cat_name
		,replace_tab_by_spaces: 2
		,is_editable: is_improve
		,font_size: 10
		,toolbar: "search, go_to_line, fullscreen, |, undo, redo, |, select_font, |, syntax_selection, |, change_smooth_selection, highlight, reset_highlight"
		,syntax_selection_allow: "css,html,js,php,python,vb,xml,c,cpp,sql,basic,pas,brainfuck"
	});
});