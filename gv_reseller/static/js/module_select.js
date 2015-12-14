var __rsGlobal = {};

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
		bindUserCountTag();
		continueBtn();
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
					var obj = targetObj[lbl.attr('title')] = {
						base: lbl.attr('listprice'),
						ppid: lbl.attr('ppid')
					};
					__rsGlobal.summary.addModule(obj);
				} else {
					__rsGlobal.summary.removeModule(targetObj[lbl.attr('title')]);
					delete targetObj[lbl.attr('title')];
				}
			}
		}
		function bindUserCountTag(){
			$('#client_count').on('change', function(){
				var val = $(this).val();
				__rsGlobal.summary.setUsers(val);
			});
		}
		function continueBtn(){
			$('#continue_btn').on('click', function(){
				var data = validateForm();
				if (!data) {
					return;
				}
				var data2 = {
					mppids: __rsGlobal.util.getMppids(),
					oppids: __rsGlobal.util.getOppids(),
					service: __rsGlobal.util.getService(),
					user: __rsGlobal.util.getUser()
				};
				data  = jQuery.extend(data, data2);
				console.log(data);
				$.post('/pricing', data, function(rs){
					//console.log('completed', rs);
					window.location = '/projects';
				});
			});
		}
	/** INIT FUNCTIONS END */

	/* some validation stuff.. */
	function validateForm(){
		var fieldVals = {};
		fieldVals['Company Name'] = $('#co_name').val();
		fieldVals['Business Registration No'] = $('#co_biz_no').val();
		fieldVals['Address 1'] = $('#co_addr1').val();
		fieldVals['Address 2'] = $('#co_addr2').val();
		fieldVals['Company Mobile'] = $('#co_mob_no').val();

		fieldVals['Point of Contact Title'] = $('#poc_title').val();	
		fieldVals['Point of Contact Name'] = $('#poc_name').val();	
		fieldVals['Point of Contact Email'] = $('#poc_email').val();
		fieldVals['Point of Contact Mobile'] = $('#poc_mob_no').val();
		fieldVals['Point of Contact Remarks'] = $('#poc_remarks').val();

		var requireFields = ['Company Name', 
			'Business Registration No',
			'Point of Contact Title',
			'Point of Contact Name'].reverse();

		var valid = true;

		for (var i = requireFields.length - 1; i >= 0; i--) {
			if ( !fieldVals[requireFields[i]] ){
				alert(requireFields[i] + ' is required.');
				valid = false;
				break;
			}
		};

		return valid ? fieldVals : false;
	}
	/***/

	__rsGlobal.util = {
		updateTotal: function(){
			var stotal = __rsGlobal.summary.getServicePrice(),
				mtotal = __rsGlobal.summary.getModulePrice(),
				utotal = __rsGlobal.summary.getUsersPrice(),
				gtotal = stotal + total + mtotal + utotal;
			$('#total_amt').html('$' + gtotal);
		},
		getMppids: function(){
			var ppids = [];
			var obj = __rsGlobal.summary.getState();
			obj.modules.forEach(function(v){
				ppids.push(v.ppid);
			});
			return ppids.join(',');
		},
		getOppids: function(){
			var ppids = [];
			var obj = __rsGlobal.summary.getState();
			obj.optional.forEach(function(v){
				ppids.push(v.ppid);
			});
			return ppids.join(',');
		},
		getService: function(){
			var rs = [];
			var obj = __rsGlobal.summary.getState();
			obj.services.forEach(function(v){
				var t = [];
				if (typeof v.extra === 'object') {
					t.push(v.title + ' - ' + v.extra[obj.wd].pages + ' Pages');					
					t.push((v.price + v.extra[obj.wd].price));
				} else {
					t.push(v.title);
					t.push(v.price);	
				}
				rs.push(t.join(';'));
			});
			return rs.join('|');
		},
		getUser: function(){
			var obj = __rsGlobal.summary.getState();
			return obj.users[0];
		}
	};

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