(function($){
	var selected_module = {},
		selected_module_elem = $('#summary_list_modules');

	var module_ppid = [],
		service_ppid = [];

	var year = 1,
		total = 0;
	var module_list_elem_tpl = [
		'<div class="row">',
		'<div class="col-sm-6">','value','</div>',
		'<div class="col-sm-6">','value','</div>',
		'</div>'
	]; //replace values of index: 2 and 5

	/******************************************************************/

	init();
	function init(){
		__retrieveGoogleFonts();
		__polyfillSticky();

		$('label.module-select').find('input').prop('checked', false);
		registerModuleSelectEvents();
	}

	/** INIT FUNCTIONS START */
		function registerModuleSelectEvents(){
			$('label.module-select').on('click.module_select', _moduleSelectHandler);
			function _moduleSelectHandler(){
				var lbl = $(this),
					targetObj = selected_module,
					isSelected = !lbl.find('input').prop('checked');

				lbl.find('input').prop('checked', isSelected);

				if (!!isSelected) {
					targetObj[lbl.attr('title')] = {
						base: lbl.attr('listprice'),
						ppid: lbl.attr('ppid')
					};
				} else {
					delete targetObj[lbl.attr('title')];
				}

				updateSummary();
			}
		}
		function updateSummary(){
		selected_module_elem.empty();
		total = 0;
		module_ppid.length = 0;
		extractData(selected_module, selected_module_elem);

		function extractData(targetObj, targetElem){
			var keys = Object.keys(targetObj);
			for (var i = keys.length - 1; i >= 0; i--) {
				var temp = module_list_elem_tpl.slice(0),
					key = keys[i],
					amount = Number(targetObj[key].base);

				temp[2] = key;
				temp[5] = '$' + amount.toFixed(2);
				targetElem.append(temp.join(''));

				total = total + amount;
				module_ppid.push(targetObj[key].ppid);
			}
		}

		if(selected_module_elem.children().length === 0)
			selected_module_elem.html('No module selected');			

		$('#total_amt').html('$' + total);
	}
	/** INIT FUNCTIONS END */

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
			return Object.keys(selected_module).length;
		}
	/** UTIL FUNCTIONS END **/

	/** REACT CODE START */
		
	/** REACT CODE END */

	/** EXTERNALS */
	function __polyfillSticky(){
		var stickyElements = document.getElementsByClassName('sticky');

		for (var i = stickyElements.length - 1; i >= 0; i--) {
		    Stickyfill.add(stickyElements[i]);
		}
	}
	function __retrieveGoogleFonts(){
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
})(jQuery);