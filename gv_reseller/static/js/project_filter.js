(function($){
	$(document).ready(function() { 
	  $('.gv_reseller-status-filter tr td').each(function(){
	   $(this).click(function(){
	      $('.gv_reseller-line-up-arrow').removeClass('gv_reseller-line-up-arrow')
	      $(this).find('hr').addClass('gv_reseller-line-up-arrow')
	      
	   })

	  })
	  
	  
	  
	  
	  
	  
	  
	});
})(jQuery);