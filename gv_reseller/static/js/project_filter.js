(function($){
	var status_index;
	var filter_status = "";
	
	$(document).ready(function() { 
		
		set_project_table_status_index();
		$('.gv_reseller-status-filter tr td').each(function(){
			$(this).click(function(){
				$('.gv_reseller-line-up-arrow').removeClass('gv_reseller-line-up-arrow');
				$(this).find('hr').addClass('gv_reseller-line-up-arrow');
				$('#input-search-filter')[0].value = '';
				filter_status = $(this)[0].getAttribute('value');
				filter(filter_status);
			})
		})
	  
		$('#button-search-filter').click(function(){
			filter(filter_status,  $('#input-search-filter')[0].value);
		})
		
		$('.gv_reseller-project-table').tablesorter();
		
	    $('.gv_reseller-approve-button').click(function(){
	        var project_id = $(this)[0].id;
	        jQuery.get('/projects/approve-project',{
	                project_id: project_id
	            }, function(rs){
	                location.reload();
	            });
	    });
	    
	    $('.gv_reseller-reject-button').click(function(){
	        var project_id = $(this)[0].id;
	        jQuery.get('/projects/reject-project',{
	                project_id: project_id
	            }, function(rs){
	                location.reload();
	            });
	    });
	    
	    $('.gv_reseller-project-table tr:nth-child(n+1)').click(function(){
	        var project_id = $(this)[0].id;
	        $('#gv_reseller-input-id').val(project_id);
	        $('#form-project-details')[0].submit();
	    });

	});
	
	function set_project_table_status_index(){
		for (var j = 0, col; col = $('.gv_reseller-project-table tr')[0].cells[j]; j++) {
			if (col.innerHTML.toLowerCase().indexOf('status') != -1){
				status_index = j;
				return;
			}
		}
	}
		
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
	
	function table_row_contains(table_row, search_string){
		for (var j = 0, col; col = table_row.cells[j]; j++) {
			if (compare_ignore_case(col.innerHTML, search_string)){
				return true;
			}
		}
		return false;
	}
	
	function compare_ignore_case(string, searchword){
		if (string==null || searchword==null){
			console.log('compare_ignore_case has a null value: ' + string + ' : ' + searchword);
			return false;
		}
		return string.toString().toLowerCase().indexOf(searchword.toString().toLowerCase())>-1;
	}
})(jQuery);