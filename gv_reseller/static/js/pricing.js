var __rsGlobal = {
	isEditable: true,
	observer: {
		callCount: 0,
		obs_list: [],
		add: function(hndl){
			this.obs_list.push(hndl);
		},
		notify: function(){
			if (this.callCount > 0) return;
			for(var i = 0, max = this.obs_list.length; i < max; i++){
				this.obs_list[i]();
			}
			this.callCount++;
		}
	},
	closeOverLay: function() {
		$('.pricing_overlay').fadeOut();
	},
	page: getUrlVars().pages || 1
};

(function($){
	var selected_module = {}, total = 0;

	init();
	function init(){
		// Unchecks all checkboxes pre-checked by the browser
		$('label.module-select').find('input').prop('checked', false);
		registerModuleSelectEvents();
		bindUserCountTag();
		togglePages();


		//Registers an event to trigger when all JSX files are loaded
		__rsGlobal.observer.add(function(){
			var project_id = getProjectId();
			if (!!project_id) {
				jQuery.get('/pricing/project-details?project_id='+project_id, function(rs){
					populateFields(JSON.parse(rs));
				});
			}
			continueBtn();
			setTimeout(function(){__rsGlobal.closeOverLay();},150);
		});
		__retrieveGoogleFonts();
		__polyfillSticky();
	}

	/** INIT FUNCTIONS START */
		function togglePages(){
			var backBtn = jQuery(jQuery('.btm_nav div')[0]).css({'visibility':'hidden'}),
				nextBtn = jQuery(jQuery('.btm_nav div')[1]).css({'visibility':'initial'});
			jQuery('[id^="pane"]').hide();
			jQuery('[id="pane' + __rsGlobal.page).show();
			jQuery(jQuery('#rs_pagination').find('ul li')[(__rsGlobal.page - 1)]).addClass('active')
			jQuery('#rs_pagination').find('ul li').each(function(i){
				jQuery(this).on('click', function(){
					__rsGlobal.page = i + 1;
					togglePaginationStyles();
					toggleNavControls();				
				});
			});

			backBtn.on('click', function(){
				if (__rsGlobal.page !== 1) {	
					__rsGlobal.page -= 1;				
					togglePaginationStyles();
					toggleNavControls();
				}
			});

			nextBtn.on('click', function(){
				if (__rsGlobal.page !== 4) {	
					__rsGlobal.page += 1;				
					togglePaginationStyles();
					toggleNavControls();
				}
			});

			function toggleNavControls(){
				var index = __rsGlobal.page;
				backBtn.css({'visibility':'initial'});
				nextBtn.css({'visibility':'initial'});
				if (index === 1) 
					backBtn.css({'visibility':'hidden'});
				if (index === 4) 
					nextBtn.css({'visibility':'hidden'});
			}

			function togglePaginationStyles(){				
				jQuery('#rs_pagination').find('ul li').removeClass('active');
				jQuery(jQuery('#rs_pagination').find('ul li')[__rsGlobal.page - 1]).addClass('active');
				jQuery('[id^="pane"]').hide();
				jQuery('[id^="pane'+(__rsGlobal.page)+'"]').show();
			}
		}

		function populateFields(data){
			var company = data.company;
			$('#co_name').val(company['Company Name']).attr('disabled', 'disabled');
			$('#co_biz_no').val(company['Business Registration No']).attr('disabled', 'disabled');
			$('#co_addr1').val(company['Address 1']).attr('disabled', 'disabled');
			$('#co_addr2').val(company['Address 2']).attr('disabled', 'disabled');
			$('#co_mob_no').val(company['phone']).attr('disabled', 'disabled');
			$('#co_email').val(company['email']).attr('disabled', 'disabled');
			$('#co_post_code').val(company['Postal Code']).attr('disabled', 'disabled');

			var contact = data.contact;
			$('#poc_title').val(contact['honorifics']).attr('disabled', 'disabled');	
			$('#poc_name').val(contact['name']).attr('disabled', 'disabled');	
			$('#poc_email').val(contact['email']).attr('disabled', 'disabled');
			$('#poc_mob_no').val(contact['mobile']).attr('disabled', 'disabled');
			$('#poc_remarks').val(contact['remarks']).attr('disabled', 'disabled');

			var products = data.sale_order_line;
				console.log(products);
			var productIndex = {};
			for (var i = products.length - 1; i >= 0; i--) {
				productIndex[products[i].name] = i;
				var cb_selector = 'label[title="'+products[i].name+'"] .cb_module';
				$(cb_selector).prop('checked', true);
				var lbl = $('label[title="'+products[i].name+'"]');
				if (lbl.length > 0) {
					var obj = selected_module[lbl.attr('title')] = {
						base: lbl.attr('listprice'),
						ppid: lbl.attr('ppid')
					};
					__rsGlobal.summary.addModule(obj);
				} else if (!!opsvTmpl[products[i].name]) {
					var searchArray = opsvTmpl[products[i].name].variants;
					var index;
					for (var j = searchArray.length - 1; j >= 0; j--) {
						if (searchArray[j].ppid == products[i].ppid){
							index = j; break;
						}
					};
					__rsGlobal[products[i].name].setState(index);
				} else if (!!otsvTmpl[products[i].name]) {
					__rsGlobal[products[i].name].setState(true);
				} else if (products[i].name.indexOf('Website Design') > -1) {
					var num = parseInt(products[i].name.split(' ')[3]) > 10 ? 1 : 0 ;
					__rsGlobal['Website Design'].setPages(num);
				} else if (products[i].name === 'Email Hosting'){
					__rsGlobal['Email Hosting'].setState(true);
				} else if (products[i].name === 'Website Domain(.COM)'){
					__rsGlobal['Website Domain1'].setState(true);
				} else if (products[i].name === 'Website Domain(.COM.SG)'){
					__rsGlobal['Website Domain2'].setState(true);
				} else if (products[i].name === 'Website Domain(.SG)'){
					__rsGlobal['Website Domain3'].setState(true);
				}
			}

			//disable editting
			var proxied = $._data($('label.module-select').get(0), "events").click[0].handler;
			$('label.module-select').off('click.module_select').on('click.module_select', function(){
				if(__rsGlobal.isEditable === true){
					proxied.apply(this, arguments);
				} else {
					return;
				}
			}).find('.cb_module').attr('disabled','disabled');
			$('#client_count').val(products[productIndex['Number of Users']].qty).attr('disabled', 'disabled');
			__rsGlobal.summary.setUsers(products[productIndex['Number of Users']].qty);
			$('.left2').css({'pointerEvents':'none'})
			__rsGlobal.isEditable = false;

			$('#page_title').html('Project Subscription');
			$('#continue_btn, #request_quote_btn').hide();

			//create project details table
			var project = data.project;

			var sales_name = createElem('div.col-sm-4', [createElem('label','Name'),createElem('input#sales_name.form-control[disabled=disabled][value='+project.rs_name+']')]);
			var sales_contact = createElem('div.col-sm-4', [
				createElem('label','Contact No.'),
				createElem('div.input-group',[
						createElem('span.input-group-addon', '+65'), 
						createElem('input#sales_contact.form-control[disabled=disabled][value='+project.rs_contact+']')
					])
				]);
			var sales_email = createElem('div.col-sm-4', [createElem('label','Email Address'),createElem('input#sales_email.form-control[disabled=disabled][value='+project.rs_email+']')]);
			var salesPersonDiv = createElem('div.row', [sales_name,sales_contact,sales_email]);
			$('#form_div').prepend(salesPersonDiv);
			$('#form_div').prepend(createElem('h3','Sales Person Details'));

			var projectId = createElem('div.col-sm-4', [createElem('label', 'Project ID'), project.id]);
			var startDate = createElem('div.col-sm-4', [createElem('label', 'Start Date'), !!project.project_start_date ? project.project_start_date : '-']);
			var status = createElem('div.col-sm-4', [createElem('label', 'Status'), project.status]);
			var createDate = createElem('div.col-sm-4', [createElem('label', 'Created Date'), project.created_date]);
			var expiryDate = createElem('div.col-sm-4', [createElem('label', 'Expiry Date'), !!project.project_end_date ? project.project_end_date : '-' ]);
			var currentPrice = createElem('div.col-sm-4', [createElem('label', 'Current Price'), isRSA ? '$'+project.total.toFixed(2) : '-']);
			var projectDetailsDiv = createElem('div.row.project_details',[createElem('h3.col-sm-12','Project Details'),projectId,startDate,status,createDate,expiryDate,currentPrice]);
			$('#form_div').prepend(projectDetailsDiv);

			//addition of buttons
			if (isRSA) {
				if (project.status === 'pending') {
					$('.action_div').append('<div id="approve_btn" style="margin-top:10px;" class="btn-green">Approve</div>');
					$('.action_div').append('<div id="reject_btn" style="margin-top:10px;" class="btn-green">Reject</div>');
				} else if (project.status == 'approved') {
					$('.action_div').append('<div id="reject_btn" style="margin-top:10px;" class="btn-green">Reject</div>');
				}
				var data = { project_id: project.id };
				$('#approve_btn').on('click', function(){
					$('#gv_reseller-approve-modal').modal('show');
				});
				$('#terms').on('click', function(){
					if (this.checked){
						$('#confirm-approve_btn').removeClass('gv_reseller-btn-disabled');
					}
					else {
						$('#confirm-approve_btn').addClass('gv_reseller-btn-disabled');
					}
					console.log(this.checked);
				});
				$('#confirm-approve_btn').on('click', function(){
					if ($('#terms')[0].checked){
						$.get('/projects/approve-project', data).then(function(){
							location.href = '/projects';
						});				
					}
				});
				
				$('#reject_btn').on('click', function(){ 
					$('#gv_reseller-reject-modal').modal('show');
					$('#gv_reseller-submit-reject').hide();
					$('#gv_reseller-confirm-reject').show();
				});	
				$('#confirm-reject_btn').on('click', function(){
					$('#gv_reseller-confirm-reject').hide();
					$('#gv_reseller-submit-reject').show();
				});
				$('#submit-reject_btn').on('click', function(){
					data.reject_feedback = $('#gv_reseller-reject-feedback').val();
					$.get('/projects/reject-project', data).then(function(){
						location.href = '/projects';
					});
				});
			}
			if (project.status === 'pending') {
				$('.action_div').append('<div id="edit_btn" style="margin-top:10px;" class="btn-green">Edit</div>');	
				$('#edit_btn').on('click', function(){
					__rsGlobal.isEditable = true;
					$('label.module-select .cb_module').removeAttr('disabled');				
					$('#client_count').removeAttr('disabled');
					$(this).hide();
					$('#continue_btn').html('Save').show();
					$('.left2').css({'pointerEvents':'all'})
					$("#custom_form input, #custom_form textarea").removeAttr('disabled');
				});
			}			
			$('.action_div').append('<a href="/projects"><div id="back_btn" style="margin-top:10px;" class="btn-green">Back</div></a>');
		}

		function getProjectId(){
			return getParameterByName('project_id');
			function getParameterByName(name) {
			    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
			    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
			        results = regex.exec(location.search);
			    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
			}
		}

		function registerModuleSelectEvents(){
			$('label.module-select').on('click.module_select', _moduleSelectHandler);
			function _moduleSelectHandler(){
				var lbl = $(this),
					targetObj = selected_module,
					isSelected = !lbl.find('input').prop('checked');

				lbl.find('input[type=checkbox]').prop('checked', isSelected);
				
				if (isSelected === false) {
					lbl.find('input[type=hidden].dpt').each(function(i,el){
						var target = $('label.module-select[ppid='+$(el).val()+']'),
							isChecked = target.find('input[type=checkbox]').prop('checked');

						if (isChecked === true)
							target.trigger('click.module_select');
					});
				} else {
					lbl.find('input[type=hidden].dpc').each(function(i,el){
						var target = $('label.module-select[ppid='+$(el).val()+']'),
							isChecked = target.find('input[type=checkbox]').prop('checked');
						if (isChecked === false)
							target.trigger('click.module_select');
					});
				}

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
 			var minus_btn = $('.rs_number_slider span')[0], 			
 				plus_btn = $('.rs_number_slider span')[2];

 			$(minus_btn).on('click', function(){
 				if (parseInt($('#client_count').val()) === 1) return;
 				$('#client_count').val( parseInt($('#client_count').val()) - 1 );
 				clientCountOnChange();
 			});
 			$(plus_btn).on('click', function(){
 				$('#client_count').val( parseInt($('#client_count').val()) + 1 );
 				clientCountOnChange();
 			});

 			$('.rs_number_slider b').html('$' + per_user_price);
			$('#client_count').on('change', clientCountOnChange);

			function clientCountOnChange(){
				var val = $('#client_count').val();
				__rsGlobal.summary.setUsers(val);
				$('.rs_number_slider val').html('' + val);
			}
		}

		function continueBtn(){
			$('#continue_btn').on('click', function(){
				var data = validateForm();
				if (!data) {
					return;
				}
				if (getProjectId())
					data.project_id = getProjectId();
				var data2 = {
					mppids: __rsGlobal.util.getMppids(),
					oppids: __rsGlobal.util.getOppids(),
					service: __rsGlobal.util.getService(),
					user: __rsGlobal.util.getUser()
				};
				data  = jQuery.extend(data, data2);
				$.post('/pricing', data, function(rs){
					window.location = '/projects';
				});
			});
		}

	/** INIT FUNCTIONS END */

	/* CLIENT DETAILS FORM VALIDATION */
	function validateForm(){
		var fieldVals = {};
		fieldVals['Company Name'] = $('#co_name').val();
		fieldVals['Business Registration No'] = $('#co_biz_no').val();
		fieldVals['Address 1'] = $('#co_addr1').val();
		fieldVals['Address 2'] = $('#co_addr2').val();
		fieldVals['Company Mobile'] = $('#co_mob_no').val();
		fieldVals['Company Email'] = $('#co_email').val();
		fieldVals['Postal Code'] = $('#co_post_code').val();

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

	function createElem(tagName, inner){
		var element, id, classNames=[], tag, attrs=[];

		if (!!tagName.match(/\[(.*?)\]/g)) {
			attrs = tagName.match(/\[(.*?)\]/g);
			tagName = tagName.replace(/\[(.*?)\]/g, '');
			console.log(attrs, tagName);
		}
		classNames = tagName.split('.');
		id = classNames[0].split('#')[1];
		tag = classNames.shift().split('#')[0];				
		element = document.createElement(tag);

		if (classNames.length > 0)
			element.setAttribute('class', classNames.reduce(function(p, c){return p + ' ' + c; }));
		if (id !== undefined)
			element.setAttribute('id', id);
		if (attrs.length > 0) {
			attrs.forEach(function(attr){
				attr = attr.substring(1, attr.length-1).split('=');
				element.setAttribute(attr[0], attr[1]);
			});
		}

		if (inner === undefined) return element;
		appendInner(inner);
		function appendInner(_inner){
			if (_inner.constructor === Array) {						
				for (var x in _inner){
					appendInner(_inner[x]);
				}
			} else if(_inner instanceof Element) {
				element.appendChild(_inner);
			} else {
				element.appendChild(document.createTextNode(_inner));
			}
		}

		return element;
	}

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

/** Utility Functions */
/**
 * getUrlVars
 * Get the query string from URL
 * @return {Object} "Key" will be the name of the Param
 */
function getUrlVars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}