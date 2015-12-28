(function($){
	var status_index;
	var filter_status = "";
	
	$(document).ready(function() { 
		
		set_project_table_status_index();
		// animates the upward pointer for selected status filter in the page.
		// also resets the search filter values to empty string.
		$('.gv_reseller-status-filter tr td').each(function(){
			$(this).click(function(){
				$('.gv_reseller-line-up-arrow').removeClass('gv_reseller-line-up-arrow');
				$(this).addClass('gv_reseller-line-up-arrow');
				$('#input-search-filter')[0].value = '';
				filter_status = $(this)[0].getAttribute('value');
				filter(filter_status);
			})
		})
	  
		// appends the filter function to the search button
		$('#button-search-filter').click(function(){
			filter(filter_status,  $('#input-search-filter')[0].value);
		})
		
		// allows the table to be sorted by clicking the table header.
		$('.gv_reseller-project-table').tablesorter();
		
	 // binds view buttons to send a get request to the server to view the project
	    $('.gv_reseller-view-button').click(function(){
	        var project_id = $(this)[0].id;
	        $('#gv_reseller-input-id').val(project_id);
	        $('#form-project-details')[0].submit();
	    });
	});
	
	// sets the index number of the status column in gv_reseller-project-table. This value is used as a shortcut to retrieve every row's project status
	// for filtering purposes.
	function set_project_table_status_index(){
		for (var j = 0, col; col = $('.gv_reseller-project-table tr')[0].cells[j]; j++) {
			if (col.innerHTML.toLowerCase().indexOf('status') != -1){
				status_index = j;
				return;
			}
		}
	}
		
	// @params: status_string: string, search_string: string 
	// filter function that hides the rows that do not have the correct status or does not contain the search word.
	function filter(status_string, search_string){
		status_string = status_string || ''; //converts undefined to empty string
		search_string = search_string || ''; //converts undefined to empty string
		
		for (var i = 1, row; row = $('.gv_reseller-project-table')[0].rows[i]; i++) {
			var match = compare_ignore_case(row.cells[status_index].innerHTML, status_string);
			if (match){
				match = table_row_contains(row, search_string);
			}
			if (match){
				$(row).removeClass('hidden');
			}
			else {
				$(row).addClass('hidden');
			}
		}
	}
	
	// @params: table_row: integer, search_string: string
	// goes through every table cell of the row and returns true if the cell values contains the search_string. Otherwise, return false.  
	function table_row_contains(table_row, search_string){
		for (var j = 0, col; col = table_row.cells[j]; j++) {
			if (compare_ignore_case(col.innerHTML, search_string)){
				return true;
			}
		}
		return false;
	}
	
	// @params: string: string, searchword: string 
	// returns true if string contains searchword. Ignores case sensitivity.
	function compare_ignore_case(string, searchword){
		if (string==null || searchword==null){
			console.log('compare_ignore_case has a null value: ' + string + ' : ' + searchword);
			return false;
		}
		return string.toString().toLowerCase().indexOf(searchword.toString().toLowerCase())>-1;
	}
})(jQuery);