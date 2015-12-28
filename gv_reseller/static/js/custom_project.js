(function($){
	var status_index;
	var filter_status = "";
	
	$(document).ready(function() { 
		toggle_edit($('#project_id')[0].value == 0);
		
		$('.gv_reseller_custom_project_submit').click(function(){
			$('#gv_reseller_custom-project-submit-button').click();
		})
	})
    
	//toggles between view mode and edit mode for the form.
    function toggle_edit(edit){
		if (edit){
			$('.gv_reseller-custom-form-control input').show();
			$('.gv_reseller-project-info-display').hide();
			$('#gv_reseller_custom_project_submit').show();
			$('.gv_reseller-phone-control-area-code').show();
			$('textarea').show();
		}
		else {
			$('.gv_reseller-custom-form-control input').hide();
			$('.gv_reseller-project-info-display').show();
			$('#gv_reseller_custom_project_submit').hide();
			$('.gv_reseller-phone-control-area-code').hide();
			$('textarea').hide();
		}
    }
})(jQuery);