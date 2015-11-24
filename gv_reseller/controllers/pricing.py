from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp import SUPERUSER_ID
from datetime import datetime

import json

def pretty(d, indent=0):
   for key, value in d.iteritems():
      print '\t' * indent + str(key)
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print '\t' * (indent+1) + str(value)

class booking(http.Controller):

	#Handles the GET request for the route '/bookings'
	@http.route(
		['/pricing'],
		auth='user',
		methods=['get'],
		website=True)
	def booking_get(self):

		consu_product_templates = request.env['product.template'].search([('type','=','consu')])
		consu_product_product = {}

		for x in consu_product_templates:
			consu_product_product[x] = request.env['product.product'].search([('product_tmpl_id', '=', x.id)])
			for attr in dir(x):
				print attr

		return http.request.render('gv_reseller.pricing', {
			'consu_product_templates': consu_product_templates,
			'consu_product_product': consu_product_product,
			'user': request.env.user
		})



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