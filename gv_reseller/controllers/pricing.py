from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp import SUPERUSER_ID
from datetime import datetime

import json

class booking(http.Controller):

	#Handles the GET request for the route '/pricing'
	@http.route(
		['/pricing'],
		auth='user',
		methods=['get'],
		website=True)
	def pricing_get(self):
		consu_product_templates = request.env['product.template'].search([('type','=','module')])
		consu_product_product = {}

		misc_product_templates = request.env['product.template'].search([('type','=','misc')])
		misc_product_product = {}

		other_product_templates = request.env['product.template'].search([('type','=','other')])
		other_product_product = {}

		optional_product_templates = request.env['product.template'].search([('type','=','optional')])
		optional_product_product = {}
		optional_product_product_base = {}

		for x in consu_product_templates:
			consu_product_product[x] = request.env['product.product'].search([('product_tmpl_id', '=', x.id)])
		for x in misc_product_templates:
			misc_product_product[x] = request.env['product.product'].search([('product_tmpl_id', '=', x.id)])
		for x in other_product_templates:
			other_product_product[x] = request.env['product.product'].search([('product_tmpl_id', '=', x.id)])
		for x in optional_product_templates:
			optional_product_product[x] = request.env['product.product'].search([('product_tmpl_id', '=', x.id)])

		print dir(optional_product_templates[0])
		print optional_product_templates[0].product_variant_ids
		print optional_product_product

		# print dir(optional_product_templates)
		# print optional_product_templates.attribute_line_ids

		# print dir(optional_product_templates.attribute_line_ids[0])
		# print optional_product_templates.attribute_line_ids[0]
		# print optional_product_templates.attribute_line_ids[0].display_name
		# print optional_product_templates.attribute_line_ids[1].display_name

		# print dir(request.env.ref('gv_reseller.product_att_impl'))

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

		pplist = pp.browse(kw['ppids'].split(','))
		print 'HERE '
		#print pplist[0].product_tmpl_id
		# return

		#perform validation if ppids has val
		print kw['ppids'].split(',')

		soc = request.website.sale_get_order(force_create=1);	
		soc.write({'order_line': [(5,)] })
		soc = request.website.sale_get_order(force_create=1);

		soid = soc.id
		# 	'partner_id': request.env.user.partner_id.id,
		# 	'state': 'draft',
		# })

		sollist = []
		for x in kw['ppids'].split(','):
			print pp.search([('id','=',x)])[0].product_tmpl_id
			solid = sol.sudo().create({
				'name': '-',
				'product_id': pp.search([('id','=',x)])[0].id,
				'order_id': soid
			})
			print solid
			sollist.append((4,solid.id))


		print sollist;
		soc.write({'order_line': sollist })

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