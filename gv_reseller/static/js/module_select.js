(function($){
	var selected_module = {},
		selected_module_elem = $('#summary_list_modules');
	var selected_module_misc = {},
		selected_module_misc_elem = $('#summary_list_modules_misc');
	var selected_service = {},
		selected_service_elem =	$('#summary_list_service');

	var module_ppid = [],
		service_ppid = [];

	var year = 1,
		total = 0,
		service_total = 0;
	var module_list_elem_tpl = [
		'<div class="row">',
		'<div class="col-sm-6">','value','</div>',
		'<div class="col-sm-6">','value','</div>',
		'</div>'
	]; //replace values of index: 2 and 5

	function collatePIDs(){
		return module_ppid.concat(service_ppid);
	}

	init();
	function init(){
		$('label.module-select').find('input').prop('checked', false);
		updateDisplayPrice();
		retrieveGoogleFonts();
		registerServiceSelection();
		registerModuleSelection();
	}

	function registerModuleSelection(){
		$('label.module-select').on('click', function(){
			var lbl = $(this),
				isSelected = !lbl.find('input').prop('checked'),
				targetObj = lbl.hasClass('misc') ? selected_module_misc : selected_module;

			lbl.find('input').prop('checked', isSelected);
			if (!!isSelected) {
				targetObj[lbl.attr('title')] = {
					base: lbl.attr('listprice'),
					year1: {
						price: lbl.find('m-data[year="1"]').attr('price'),
						ppid: lbl.find('m-data[year="1"]').attr('ppid')
					},
					year2: {
						price: lbl.find('m-data[year="2"]').attr('price'),
						ppid: lbl.find('m-data[year="2"]').attr('ppid')
					},
					year3: {
						price: lbl.find('m-data[year="3"]').attr('price'),
						ppid: lbl.find('m-data[year="3"]').attr('ppid')
					}
				}
			} else {
				delete targetObj[lbl.attr('title')];
			}
			updateList();
		});

		$('.summary_tabs .tab').on('click', function(){
			$('.summary_tabs .tab').removeClass('active');
			$(this).addClass('active');
			year = $(this).attr('val');
			updateList();
			updateDisplayPrice();
		});
	}

	function registerServiceSelection(){
		$('input.cb_service').each(function(i,elem){
			$(elem).on('change', function(){
				if ($(this).prop('checked')) {
					$('input.cb_service[cname="'+$(this).attr('cname')+'"]').prop('checked', false);
					$(this).prop('checked', true);
					selected_service[$(this).attr('title')] = {
						'title': $(this).attr('title'),
						'price': $(this).val(),
						'ppid': $(this).attr('ppid')
					};
				} else {
					delete selected_service[$(this).attr('title')];
				}
				updateServiceList();
			})
		});
	}

	function updateDisplayPrice(){
		$('label.module-select').each(function(i, elem){
			var l_price = Number($(elem).attr('listprice'));
			var e_price = Number($(elem).find('m-data[year="'+year+'"]').attr('price'));
			$(elem).find('.module_price').html('S$' + (e_price + l_price).toFixed(2));
		});
	}

	function retrieveGoogleFonts(){
		WebFontConfig = {
			google: { families: [ 'Lato:400,100,300,700,900:latin' ] }
		};
		(function() {
			var wf = document.createElement('script');
			wf.src = ('https:' == document.location.protocol ? 'https' : 'http') +
			  '://ajax.googleapis.com/ajax/libs/webfont/1/webfont.js';
			wf.type = 'text/javascript';
			wf.async = 'true';
			var s = document.getElementsByTagName('script')[0];
			s.parentNode.insertBefore(wf, s);
		})();
	}

	function updateList(){
		selected_module_elem.empty();
		selected_module_misc_elem.empty();
		total = 0;
		module_ppid.length = 0;

		extractData(selected_module, selected_module_elem);
		extractData(selected_module_misc, selected_module_misc_elem);

		function extractData(targetObj, targetElem){
			var keys = Object.keys(targetObj);
			for (var i = keys.length - 1; i >= 0; i--) {
				var temp = module_list_elem_tpl.slice(0),
					key = keys[i],
					amount = Number(targetObj[key]['year'+year].price);
				temp[2] = key;
				temp[5] = '$' + amount.toFixed(2);
				targetElem.append(temp.join(''));

				total = total + amount;
				module_ppid.push(targetObj[key]['year'+year].ppid);
			}

		}

		if(selected_module_elem.children().length === 0)
			selected_module_elem.html('No module selected');
		if(selected_module_misc_elem.children().length === 0)
			selected_module_misc_elem.html('No misc module selected');			

		$('#total_amt').html('S$' + (total + service_total).toFixed(2));
		console.log(collatePIDs());
	}

	function updateServiceList(){
		selected_service_elem.empty();
		service_total = 0;
		service_ppid.length = 0;

		var keys = Object.keys(selected_service);
		for (var i = keys.length - 1; i >= 0; i--) {
			var temp = module_list_elem_tpl.slice(0),
				key = keys[i],
				amount = Number(selected_service[key].price);
			temp[2] = key;
			temp[5] = '$' + amount.toFixed(2);
			selected_service_elem.append(temp.join(''));

			service_total = service_total + amount;
			service_ppid.push(selected_service[key].ppid);
		}

		if(selected_service_elem.children().length === 0)
			selected_service_elem.html('No service selected');

		$('#total_amt').html('S$' + (total + service_total).toFixed(2));
		console.log(collatePIDs());
	}
})(jQuery);