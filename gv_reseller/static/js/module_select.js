(function($){
	$('label.module-select').on('click', function(){
		var lbl = $(this);
		var isSelected = lbl.find('input').prop('checked');
		lbl.find('input').prop('checked', !isSelected);
		console.log(lbl.attr('title'), isSelected);
	});
})(jQuery);