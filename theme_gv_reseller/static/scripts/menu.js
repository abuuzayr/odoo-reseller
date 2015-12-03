document.addEventListener("DOMContentLoaded", function(event) {
	console.log("DOM fully loaded and parsed");
	tMenuElem = $('#top_menu');

	$('#sidemenu').on('click', function(){
		tMenuElem.toggleClass('expand');
	});

	appendMenuBlocks();
	function appendMenuBlocks(){
		tMenuElem.find('li').each(function(i, elem){
			elem = $(elem);
			var label = elem.find('span').html();
			if (!!label) {
				elem.append('<div class="menu_label">' + label + '</div>');
			}
		})
	}
});