(function($){
	var selected_module = {},
		selected_module_elem = $('#summary_list_modules');
	var selected_module_misc = {},
		selected_module_misc_elem = $('#summary_list_modules_misc');

	var selected_service = {},
		selected_service_elem =	$('#summary_list_service');

	var module_ppid = [],
		service_ppid = [];

	var pageState = 'selection';

	var packageData = {
		'A': 3, // 1-3
		'B': 7, // 4-7
		'C': 10 // 7+
	}

	var year = 1,
		total = 0,
		service_total = 0;
	var module_list_elem_tpl = [
		'<div class="row">',
		'<div class="col-sm-6">','value','</div>',
		'<div class="col-sm-6">','value','</div>',
		'</div>'
	]; //replace values of index: 2 and 5

	/** Continue Button Event */
	$('#continue_btn').on('click', function(){
		if (collatePIDs().length === 0) {
			alert('You have not selected any modules');
			console.warn('No Selection Made, perform validation here');
			return;
		}

		toggleState();

		function toggleState(){
			if (pageState == 'selection') {
				hideAllUnselectedModules();
				setConfirmStateTexts();
			} else {
				showAllModules();
				setSelectionStateTexts();
			}

			pageState = (pageState === 'selection') ? 'confirm' : 'selection';
		}

		function setConfirmStateTexts(){			
			$('#continue_btn').attr('prevText', $('#continue_btn').html());
			$('#continue_btn').html('Back');

			$('#modules_h3').attr('prevText', $('#modules_h3').html());
			$('#modules_h3').html('Modules Selected');

			$('#no_users_div').hide();
			$('#misc_module_div').hide();

			$('.product_row .desc, .c_header').hide();
			$('#optional_service_div').hide();

			$('.cb_service').parent().hide();
			$('.cb_service').hide();
			$('.cb_service:checked').parent().show();
		}

		function setSelectionStateTexts(){			
			$('#continue_btn').html($('#continue_btn').attr('prevText'));
			$('#modules_h3').html($('#modules_h3').attr('prevText'));
			$('#no_users_div').show();
			$('#misc_module_div').show();
			$('.product_row .desc, .c_header').show();
			$('#optional_service_div').show();
			$('.cb_service').parent().show();
			$('.cb_service').show();
		}

		function hideAllUnselectedServices(){

		}

		function hideAllUnselectedModules(){
			var allSelectedModuleTitles = Object.keys(selected_module).concat(Object.keys(selected_module_misc));

			$('label.module-select').each(function(i, elem){
				elem = $(elem);
				if (elem.hasClass('misc')) {
					$('#module_div div.row').append(elem);
				}
				if (allSelectedModuleTitles.indexOf(elem.attr('title')) === -1) {
					elem.hide();
				}
				elem.off('click.module_select'); //Disables click fn
				elem.css({'cursor':'not-allowed'});
			});

			$('#misc_module_div').hide();
		}
		function showAllModules(){
			$('label.module-select').each(function(i, elem){
				elem = $(elem);
				elem.show();
				elem.on('click.module_select', _moduleSelectHandler);
				if (elem.hasClass('misc')) {
					$('#misc_module_div div.row').append(elem);
				}
				elem.removeAttr('style');
			});
		}

		// $.ajax('/pricing', { 
		// 	type:'post',
		// 	data: {
		// 	  ppids: collatePIDs().join() 
		// 	},
		// 	dataType:'html',
		// 	success: function(rs){
		// 		document.write(rs);
		// 	},
		// 	error: function(err){ console.error(err); }
		// });
	});

	init();
	function init(){
		$('label.module-select').find('input').prop('checked', false);
		updateDisplayPrice();
		updateServiceDisplayPrice();
		retrieveGoogleFonts();
		registerServiceSelection();
		registerModuleSelection();
		polyfillSticky();
	}

	function registerModuleSelection(){
		$('label.module-select').on('click.module_select', _moduleSelectHandler);

		$('.summary_tabs .tab').on('click', function(){
			$('.summary_tabs .tab').removeClass('active');
			$(this).addClass('active');
			year = $(this).attr('val');
			updateList();
			updateDisplayPrice();
		});
	}

	function _moduleSelectHandler(){
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
	}

	function registerServiceSelection(){
		$('input.cb_service').each(function(i,elem){
			$(elem).on('change', function(){
				var title = $(this).attr('title');
				if ($(this).prop('checked')) {
					$('input.cb_service[title="'+$(this).attr('title')+'"]').prop('checked', false);
					$(this).prop('checked', true);

					selected_service[title] = {
						'title': title,
						'price_options': {},
						'vtype': $(this).attr('vtype')
					};

					console.log(selected_service);
					$('input[group="'+ title +'"]').each(function(i, elem){
						selected_service[title].price_options[$(this).attr('vrnt')] = {
							'ppid': $(this).attr('ppid'),
							'price': $(this).attr('price')
						}
					});
				} else {
					delete selected_service[title];
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

	function updateServiceDisplayPrice(){
		var ptype = getCurrentPackage(getModuleCount());
		$('div.product_row').each(function(i, elem){		
			var remote_price_elem = $(this).find('input.remote + .pprice'),
				onsite_price_elem = $(this).find('input.onsite + .pprice'),
				remote_dprice = $(this).find('m-data input[vrnt="Remote_' + ptype + '"]').attr('price'),				
				onsite_dprice = $(this).find('m-data input[vrnt="On Site_' + ptype + '"]').attr('price');

			remote_price_elem.html('S$'+Number(remote_dprice).toFixed(2));
			onsite_price_elem.html('S$'+Number(onsite_dprice).toFixed(2));

			var l_price = Number($(elem).attr('listprice'));
			var e_price = Number($(elem).find('input').val());
		});

		$('.module_count').html(ptype);
		$('.module_count_range').html(getCurrentPackageRange(ptype));
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
		updateServiceDisplayPrice();
		updateServiceList();
	}

	function updateServiceList(){
		selected_service_elem.empty();
		service_total = 0;
		service_ppid.length = 0;
		var ptype = getCurrentPackage(getModuleCount()),
			keys = Object.keys(selected_service);

		for (var i = keys.length - 1; i >= 0; i--) {
			var temp = module_list_elem_tpl.slice(0),
				key = keys[i],
				vtype = selected_service[key].vtype,
				amount = Number(selected_service[key].price_options[vtype + '_' + ptype].price),
				ppid = selected_service[key].price_options[vtype + '_' + ptype].ppid;

			console.log(amount, ppid);

			temp[2] = key;
			temp[5] = '$' + amount.toFixed(2);
			selected_service_elem.append(temp.join(''));

			service_total = service_total + amount;
			service_ppid.push(ppid);
		}

		if(selected_service_elem.children().length === 0)
			selected_service_elem.html('No service selected');

		$('#total_amt').html('S$' + (total + service_total).toFixed(2));
		console.log(collatePIDs());
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
	/** UTIL FUNCTIONS START **/

		function getCurrentPackage(moduleCount){
			moduleCount = (moduleCount !== void(0)) ? moduleCount : 0;
			if (moduleCount <= packageData.A) {
				return 'A';
			} else if (moduleCount <= packageData.B){
				return 'B';
			} else {
				return 'C';
			}
		}

		function getCurrentPackageRange(ptype){
			var keys = Object.keys(packageData);
			if (keys.indexOf(ptype) === keys.length-1) {
				return packageData[keys[keys.indexOf(ptype) - 1]] + '+';
			} else if (keys.indexOf(ptype) === 0){
				return '1 - ' + packageData[ptype];
			} else {
				return '' + (packageData[keys[keys.indexOf(ptype) - 1]]+1) + ' - ' +  packageData[ptype];
			}
		}


		function collatePIDs(){
			return module_ppid.concat(service_ppid);
		}

		function getModuleCount(){
			return Object.keys(selected_module).length + Object.keys(selected_module_misc).length;
		}

	/** UTIL FUNCTIONS END **/

	function polyfillSticky(){
		var stickyElements = document.getElementsByClassName('sticky');

		for (var i = stickyElements.length - 1; i >= 0; i--) {
		    Stickyfill.add(stickyElements[i]);
		}
	}
})(jQuery);