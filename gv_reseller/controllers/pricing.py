from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp import SUPERUSER_ID
from datetime import datetime
import time
import json

class booking(http.Controller):

	#Handles the GET request for the route '/pricing'
	@http.route(
		['/pricing'],
		auth='user',
		methods=['get'],
		website=True)
	def pricing_get(self):
		consu_product_templates = request.env['product.template'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('type','=','module')])
		consu_product_product = {}

		misc_product_templates = request.env['product.template'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('type','=','misc')])
		misc_product_product = {}

		other_product_templates = request.env['product.template'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('type','=','other')])
		other_product_product = {}

		optional_product_templates = request.env['product.template'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('type','=','optional')])
		optional_product_product = {}
		optional_product_product_base = {}

		for x in consu_product_templates:
			consu_product_product[x] = request.env['product.product'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('product_tmpl_id', '=', x.id)])
		for x in misc_product_templates:
			misc_product_product[x] = request.env['product.product'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('product_tmpl_id', '=', x.id)])
		for x in other_product_templates:
			other_product_product[x] = request.env['product.product'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('product_tmpl_id', '=', x.id)])
		for x in optional_product_templates:
			optional_product_product[x] = request.env['product.product'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('product_tmpl_id', '=', x.id)])

		return http.request.render('gv_reseller.pricing', {
			'consu_product_templates': consu_product_templates,
			'consu_product_product': consu_product_product,
			'misc_product_templates': misc_product_templates,
			'misc_product_product': misc_product_product,
			'other_product_templates': other_product_templates,
			'other_product_product': other_product_product,
			'optional_product_templates': optional_product_templates,
			'optional_product_product': optional_product_product,
			'user': request.env.user
		})

	#Handles the POST request for the route '/pricing'
	@http.route(
		['/pricing'],
		auth='user',
		methods=['post'],
		website=True)
	def pricing_post(self, **kw):
		so = request.env['sale.order']
		sol = request.env['sale.order.line']
		pp = request.env['product.product']

		### get custom prod tpml id
		custom_prod_tpml = request.env.ref('gv_reseller.product_custom_tmpl')
		custom_ppid = pp.search([("product_tmpl_id", "=", custom_prod_tpml.id)])

		product_service_tmpl = request.env.ref('gv_reseller.product_service_tmpl')
		product_service_ppid = pp.search([("product_tmpl_id", "=", product_service_tmpl.id)])	

		product_user_tmpl = request.env.ref('gv_reseller.product_user_tmpl')
		product_user_ppid = pp.search([("product_tmpl_id", "=", product_user_tmpl.id)])	

		### CLEARS ANY ORDER LINE
		soc = request.website.sale_get_order(force_create=1)
		soc.write({'order_line': [(5,)] })

		soc = request.website.sale_get_order(force_create=1)
		soid = soc.id
		sollist = []

		m_price = 600.00
		if (len(kw['mppids'].split(',')) < 2):
			m_price = 1200.00

		if kw['mppids'] != "":
			for x in kw['mppids'].split(','):
				solid = sol.sudo().create({
					'name': '-',
					'product_id': pp.search([('id','=',int(x))])[0].id,
					'order_id': soid,
					'price_unit': m_price
				})
				sollist.append((4,solid.id))

		if kw['oppids'] != "":
			for x in kw['oppids'].split(','):
				print x
				solid = sol.sudo().create({
					'name': '-',
					'product_id': pp.search([('id','=',x)])[0].id,
					'order_id': soid
				})
				sollist.append((4,solid.id))

		if kw['service'] != "":
			for x in kw['service'].split('|'):
				print x
				dat = x.split(';')
				tobj = {
					'name': dat[0],
					'product_id': product_service_ppid.id,
					'order_id': soid,
					'price_unit':dat[1]
				}
				sollist.append((0,0,tobj))

		sollist.append((0,0, {
				'name': 'Number of Users',
				'product_id': product_user_ppid.id,
				'order_id': soid,
				'price_unit':product_user_ppid.lst_price,
				'product_uom_qty': kw['user']
			}))

		### Custom product example
		# sollist.append((0,0, {'name':'Custom Order Line', 'product_id':custom_ppid.id, 'order_id':soid, 'price_unit':123.45}))		
		soc.write({
			'order_line': sollist,
			'state': 'draft',
			'pricelist_id': request.env.user.property_product_pricelist.id,
	        'partner_id': request.env.user.partner_id.id,
		})

		contact = request.env['res.partner'].sudo().create({
		    'name': kw['Point of Contact Name'],
		    'mobile': kw['Point of Contact Mobile'],
		    'email' : kw['Point of Contact Email'],
		    'honorifics': kw['Point of Contact Title'], 
		    'user_id': request.env.user.id,
		    'use_parent_address': True,
		    'is_company': False,
		})

		company = request.env['res.partner'].sudo().create({
			'name': kw['Company Name'], 
			'is_company': True,
			'business_registration_number': kw['Business Registration No'],
			'street': kw['Address 1'],
			'street2': kw['Address 2'],
			'zip': kw['Postal Code'],
			'phone': kw['Company Mobile'],           
			'email' : kw['Company Email'],
			'city': 'Singapore',
			'child_ids': [(6, 0, [contact.id])],
			'user_id': request.env.user.id,
		})
		### Create A New Project		
		project = request.env['project.project'].sudo().create({
			'name': kw['Company Name'] + ' - ' + time.strftime("%c"),
			'status': 'pending',
			'sale_order': soc.id,
		    'partner_id': company.id,
			'customer_remarks': kw['Point of Contact Remarks']
		})
		
		request.website.sale_reset()
		return '200'

	#Handles the POST request for the route '/bookings'
	# @http.route(
	# 	['/bookings'],
	# 	auth='user',
	# 	methods=['post'],
	# 	website=True)
	# def booking_post(self,
	# 	package=None,
	# 	service=None,
	# 	is_from_package=None,
	# 	timeslot=None,
	# 	bookingdate=None
	# 	):

	# 	#OLD ---
	# 		print service
	# 		print bookingdate

	# 		#Models
	# 		booking_model = request.env['gv.booking']
	# 		service_model = request.env['gv.package.service']

	# 		#Instantiate a dict to store the newly gv.booking Model
	# 		booking_obj = {}

	# 		# This does date conversion, for future reference
	# 		# booking_obj['start'] = datetime.strptime(bookingdate + " " + timeslot, '%d-%m-%Y %H:%M')
	# 		booking_obj['start'] = request.env['service.scheduler'].convert_sg_datetimestring_to_utc_datetimestring(bookingdate + " " + timeslot + ":00")

	# 		booking_obj['customer'] = request.env.user.partner_id.id

	# 		#checks if the data received is a model type if so use the attribute 'id', was returning the model type before but something happened and it returns a string instead. Can't find the reason why, this is to catch any unexpected behavior
	# 		service_val = service
	# 		package_val = package
	# 		if hasattr(service, 'id'):
	# 			service_val = service.id
	# 		if hasattr(package, 'id'):
	# 			package_val = package.id

	# 		#if the booking is for a purchased package or a service, populate the related fields
	# 		if is_from_package == 'true':
	# 		 	booking_obj['is_from_package'] = True
	# 		 	booking_obj['package'] = package_val
	# 		 	booking_obj['package_service'] = service_val
	# 		else:
	# 		 	booking_obj['is_from_package'] = False
	# 			booking_obj['service'] = service_val

	# 		booking_model.create(booking_obj)

	# 		return http.request.render('gv_booking.thankyou')

	# 	#NEW ---

	# @http.route(
	# 	['/booking/timeslot'],
	# 	auth='user',
	# 	methods=['post'],
	# 	website=True)
	# def booking_timeslot(self,date,service):
	# 	# rs = request.env['service.scheduler'].get_timeslots_for_day(service, date)

	# 	# return json.dumps(rs)