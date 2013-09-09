$(document).ready(function() {
	var cat_name = $("#cat_name").val();

	// initialisation
	editAreaLoader.init({
		id: "improvedSnippetBefore"	// id of the textarea to transform		
		,start_highlight: true	// if start with highlight
		//,allow_resize: "both"
		,allow_toggle: false
		,word_wrap: true
		,language: "en"
		,syntax: cat_name
		,replace_tab_by_spaces: 2
		,is_editable: false
		,font_size: 10
		,toolbar: "search, go_to_line, fullscreen, |, undo, redo, |, select_font, |, syntax_selection, |, change_smooth_selection, highlight, reset_highlight"
		,syntax_selection_allow: "css,html,js,php,python,vb,xml,c,cpp,sql,basic,pas,brainfuck"
	});

	// initialisation
	editAreaLoader.init({
		id: "improvedSnippetAfter"	// id of the textarea to transform		
		,start_highlight: true	// if start with highlight
		//,allow_resize: "both"
		,allow_toggle: false
		,word_wrap: true
		,language: "en"
		,syntax: cat_name
		,replace_tab_by_spaces: 2
		,is_editable: false
		,font_size: 10
		,toolbar: "search, go_to_line, fullscreen, |, undo, redo, |, select_font, |, syntax_selection, |, change_smooth_selection, highlight, reset_highlight, |, help"
		,syntax_selection_allow: "css,html,js,php,python,vb,xml,c,cpp,sql,basic,pas,brainfuck"
	});
});