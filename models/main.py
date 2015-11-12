from openerp import models, fields, osv, api
from openerp.exceptions import ValidationError
import datetime

class gv_package(models.Model):
	_name = 'gv.package'

	name = fields.Char(string="Package Name", required=True)
	description = fields.Text()
	#product = fields.Many2one('product.product', string="Linked product (eCommerce)", domain=[('type','=','service')], required=True)
	service = fields.Many2one('gv.package.service', string="Linked service")
	quantity = fields.Integer(string="Quantity of service", required=True)
	active = fields.Boolean(default=True, string="Active")
	validity = fields.Many2one('gv.package.validity', string="Validity period")
	validity_in_days = fields.Integer(compute='get_validity_days', string="Validity in days")

	@api.depends('validity')
	@api.onchange('validity')
	def get_validity_days(self):
		for each in self:
			field_output = each.validity['number_of_days']
			each.validity_in_days = field_output

class gv_package_service(models.Model):
	_name = 'gv.package.service'

	_sql_constraints = [
	('name_unique',
	 'UNIQUE(name)',
	 "The name of the service must be unique."),
	]

	name = fields.Char(string="Title", required=True)
	service_availability = fields.Integer(string="Available Staff for Service")
	available_units = fields.Integer(string="Available Resources")
 	service_timeslots = fields.One2many('time.slot','service', string="Service timeslots")

	# Hours & Minutes Selection
	
	mins = [
				('00', '00'),('01', '01'),('02', '02'),('03', '03'),('04', '04'),('05', '05'),
				('06', '06'),('07', '07'),('08', '08'),('09', '09'),('10', '10'),
				('11', '11'),('12', '12'),('13', '13'),('14', '14'),('15', '15'),
				('16', '16'),('17', '17'),('18', '18'),('19', '19'),('20', '20'),
				('21', '21'),('22', '22'),('23', '23'),('24', '24'),('25', '25'),
				('26', '26'),('27', '27'),('28', '28'),('29', '29'),('30', '30'),
				('31', '31'),('32', '32'),('33', '33'),('34', '34'),('35', '35'),
				('36', '36'),('37', '37'),('38', '38'),('39', '39'),('40', '40'),
				('41', '41'),('42', '42'),('43', '43'),('44', '44'),('45', '45'),
				('46', '46'),('47', '47'),('48', '48'),('49', '49'),('50', '50'),
				('51', '51'),('52', '52'),('53', '53'),('54', '54'),('55', '55'),
				('56', '56'),('57', '57'),('58', '58'),('59', '59')
				]

	hrs = [
				('00', '00'),
				('01', '01'),('02', '02'),('03', '03'),('04', '04'),('05', '05'),
				('06', '06'),('07', '07'),('08', '08'),('09', '09'),('10', '10'),
				('11', '11'),('12', '12'),('13', '13'),('14', '14'),('15', '15'),
				('16', '16'),('17', '17'),('18', '18'),('19', '19'),('20', '20'),
				('21', '21'),('22', '22'),('23', '23'),('24', '24')
				]

	# Service Duration Timing

	service_duration_hour = fields.Selection(
				selection=hrs)

	service_duration_minute = fields.Selection(
				selection=mins)

	# Buffer Timing

	buffer_hour = fields.Selection(
				selection=hrs)

	buffer_minute = fields.Selection(
				selection=mins)

	# Start Operating Timing

	operating_start_hour = fields.Selection(
				selection=hrs)

	operating_start_minute = fields.Selection(
				selection=mins)

	# End Operating Timing

	operating_end_hour = fields.Selection(
				selection=hrs)

	operating_end_minute = fields.Selection(
				selection=mins)

	start_time = fields.Char(compute='op')
	end_time = fields.Char(compute='opend')
	service_duration = fields.Char(compute='serv_dur', string="Service Duration")
	buff_time = fields.Char(compute='buff', string="Buffer Time")
	total_time = fields.Char(compute='ophrs', string="Total Operation Hours")
	next_timeslot = fields.Char(compute='timeslots', string="Timeslot")
	repeat_times = fields.Char(compute='timeslots', string="repeat Times")
	timeslot = fields.Text(string="Timeslots")

	# Convert Service Duration String To Time Format

	@api.depends('service_duration_hour','service_duration_minute')
	def serv_dur(self):
		for each in self:
			g=float(each.service_duration_hour)
			h=float(each.service_duration_minute)
			minutes = int(round(g * 60 + h))
			each.service_duration = "%02d:%02d" % divmod(minutes, 60)

	# Convert Buffer Time String To Time Format

	@api.depends('buffer_hour','buffer_minute')
	def buff(self):
		for each in self:
			e=float(each.buffer_hour)
			f=float(each.buffer_minute)
			minutes = int(round(e * 60 + f))
			each.buff_time = "%02d:%02d" % divmod(minutes, 60)

	# Convert Starting Operating String To Time Format

	@api.depends('operating_start_hour','operating_start_minute')
	def op(self):
		for each in self:
			a=float(each.operating_start_hour)
			b=float(each.operating_start_minute)
			minutes = int(round(a * 60 + b))
			each.start_time = "%02d:%02d" % divmod(minutes, 60)


	# Convert Ending Operating String To Time Format

	@api.depends('operating_end_hour','operating_end_minute')
	def opend(self):
		for each in self:
			c=float(each.operating_end_hour)
			d=float(each.operating_end_minute)
			minutes = int(round(c * 60 + d))
			each.end_time = "%02d:%02d" % divmod(minutes, 60)

	# Calculate Total Operation Hours

	@api.depends('operating_end_hour','operating_end_minute','operating_start_hour','operating_start_minute')
	def ophrs(self):
		for each in self:
			a=float(each.operating_start_hour)
			b=float(each.operating_start_minute)
			c=float(each.operating_end_hour)
			d=float(each.operating_end_minute)
			start_minutes = int(round(a * 60 + b))
			end_minutes = int(round(c * 60 + d))
			minutes = end_minutes - start_minutes
			each.total_time = "%02d:%02d" % divmod(minutes, 60)

	# Calculate Timeslot

	@api.depends('operating_end_hour','operating_end_minute','operating_start_hour','operating_start_minute','buffer_hour','buffer_minute','service_duration_hour','service_duration_minute')
	def timeslots(self):
		for each in self:
			a=float(each.operating_start_hour)
			b=float(each.operating_start_minute)
			c=float(each.operating_end_hour)
			d=float(each.operating_end_minute)
			e=float(each.buffer_hour)
			f=float(each.buffer_minute)
			g=float(each.service_duration_hour)
			h=float(each.service_duration_minute)
			start_minutes = int(round(a * 60 + b))
			end_minutes = int(round(c * 60 + d))
			buff_minutes = int(round(e * 60 + f))
			serv_minutes = int(round(g * 60 + h))
			minutes = end_minutes - start_minutes
			total_service_time = serv_minutes + buff_minutes
			repeat = minutes/total_service_time
			slots = start_minutes + total_service_time
			start_slot = start_minutes
			time_total_service_time = "%02d:%02d" % divmod(total_service_time, 60)
			slotting = total_service_time

			count = 1
			while (count < repeat):
			   print 'Timeslot', count, ':', start_slot
			   count = count + 1
			   start_slot = start_slot + slotting

			
			each.repeat_times = repeat
			each.next_timeslot = "%02d:%02d" % divmod(slots, 60)
			
	@api.depends('service') 
	def generate_timeslots(self):
		for each in self:
			if each.service_duration:
				
				#this are stubbed quantities 
				#take from setting - configurations later
				
				opening_hour = float("09")
				opening_minute = float("30")
				closing_hour = float("21")
				closing_minute = float("00")
				
				#convert opening hour and closing hour to rounded off integers
				
				opening_convert = int(round(opening_hour * 60 + opening_minute))
				closing_convert = int(round(closing_hour * 60 + closing_minute))
				
				#calculate time difference for later loop limit
				
				time_diff = closing_convert - opening_convert
				
				#calculate total service duration
				
				duration = datetime.datetime.strptime(each.service_duration, "%H:%M")
				service_hour = float(duration.strftime("%H"))
				service_minute = float(duration.strftime("%M"))
				
				buff_time = datetime.datetime.strptime(each.buff_time, "%H:%M")
				buff_time_hour = float(buff_time.strftime("%H"))
				buff_time_minute = float(buff_time.strftime("%M"))
				
				service_convert = int(round(service_hour * 60 + service_minute))
				buff_time_convert = int(round(buff_time_hour * 60 + buff_time_minute))
				
				total_time = service_convert + buff_time_convert
				
				loop_limit = time_diff / total_time
				
				for i in range(loop_limit):
					library = self.env['time.slot']
					service_start = opening_convert + i * total_time
					start_time = "%i:%i" % (service_start / 60, service_start % 60)
					
					vals = {
							'service': each.id,
							'time_start': start_time
							}
					
					library.create(vals)

class gv_package_validity(models.Model):
	_name = 'gv.package.validity'
	
	name = fields.Char(string="Name of period", required=True)
	period = fields.Integer(string="Number of months", required=True)
	number_of_days = fields.Integer(string="Number of days", compute='months_to_days')
	
	@api.depends('period')
	@api.onchange('period')
	def months_to_days(self):
		for each in self:
			each.number_of_days = each.period * 30

class purchased_package(models.Model):
	_name = 'purchased.package'

	name = fields.Char(compute='computed_name')
	customer = fields.Many2one('res.partner', string="Customer", domain="[('customer','=',True)]", required=True)
	package = fields.Many2one('gv.package', string="Package", required=True)
	service = fields.Many2one('gv.package.service', compute='get_from_package', string="Packaged service")
	service_quantity = fields.Integer(string="Remaining service quantity")
	purchase_date = fields.Date(string="Purchase Date", default=datetime.date.today())
	package_expiry = fields.Date(string="Package Expiry", compute='final_expiry')
	validity_in_days = fields.Integer(compute='get_from_package', string="Validity in days")

	@api.onchange('customer','package')
	def computed_name(self):
		for each in self:
			if each.package['name']:
				each.name = str(each.customer['name']) + "\'s" + " " + each.package['name']

	@api.depends('package')
	@api.onchange('package')
	def get_from_package(self):
		library = self.pool.get('gv.package')
		for each in self:
			validity = each.package['validity_in_days']
			service = each.package['service']
			each.validity_in_days = validity
			each.service = service
			
	def assign_service_quantity(self):
		for each in self:
			library = self.env['gv.package'].search([('id', '=', each.package.id)])
			each.service_quantity = library['quantity']
			print each.service_quantity

	@api.depends('package','purchase_date','validity_in_days')
	def final_expiry(self):
		for each in self:
			days_to_add = each.validity_in_days
			final_date = fields.Date.from_string(each.purchase_date) + datetime.timedelta(days=days_to_add)
			each.package_expiry = final_date

class purchased_service(models.Model):
	_name = 'purchased.service'

	name = fields.Char(compute='computed_name')
	customer = fields.Many2one('res.partner', string="Customer", domain="[('customer','=',True)]", required=True)
	service = fields.Many2one('gv.package.service', string="Service")
	purchase_date = fields.Date(string="Purchase Date", default=datetime.date.today())

	@api.onchange('customer','service')
	def computed_name(self):
			for each in self:
				if each.service['name']:
					each.name = str(each.customer['name']) + "\'s" + " " + each.service['name']
		
class purchased_res_partner(models.Model):
	_inherit = 'res.partner'
	purchased_packages = fields.One2many('purchased.package','customer',string="Purchased Packages")
	purchased_services = fields.One2many('purchased.service','customer',string="Purchased Services")

class add_to_product_template(models.Model):
	_inherit = 'product.template'

	type = fields.Selection(selection_add=[
		('package', 'Package'),
		('book_service', 'Bookable Service')
		])
	package = fields.Many2one('gv.package', string="Package")
	is_package = fields.Boolean(string="This is a Package")
	is_book_service = fields.Boolean(string="This is a Bookable Service")
	service = fields.Many2one('gv.package.service', string="Linked service")
	quantity = fields.Integer(string="Quantity of service")
	validity = fields.Many2one('gv.package.validity', string="Validity period")
	
	# Hours & Minutes Selection
	
	mins = [
				('00', '00'), 
				('01', '01'),('02', '02'),('03', '03'),('04', '04'),('05', '05'),
				('06', '06'),('07', '07'),('08', '08'),('09', '09'),('10', '10'),
				('11', '11'),('12', '12'),('13', '13'),('14', '14'),('15', '15'),
				('16', '16'),('17', '17'),('18', '18'),('19', '19'),('20', '20'),
				('21', '21'),('22', '22'),('23', '23'),('24', '24'),('25', '25'),
				('26', '26'),('27', '27'),('28', '28'),('29', '29'),('30', '30'),
				('31', '31'),('32', '32'),('33', '33'),('34', '34'),('35', '35'),
				('36', '36'),('37', '37'),('38', '38'),('39', '39'),('40', '40'),
				('41', '41'),('42', '42'),('43', '43'),('44', '44'),('45', '45'),
				('46', '46'),('47', '47'),('48', '48'),('49', '49'),('50', '50'),
				('51', '51'),('52', '52'),('53', '53'),('54', '54'),('55', '55'),
				('56', '56'),('57', '57'),('58', '58'),('59', '59')
				]

	hrs = [
				('00', '00'),
				('01', '01'),('02', '02'),('03', '03'),('04', '04'),('05', '05'),
				('06', '06'),('07', '07'),('08', '08'),('09', '09'),('10', '10'),
				('11', '11'),('12', '12'),('13', '13'),('14', '14'),('15', '15'),
				('16', '16'),('17', '17'),('18', '18'),('19', '19'),('20', '20'),
				('21', '21'),('22', '22'),('23', '23'),('24', '24')
				]

	service_duration_hour = fields.Selection(selection=hrs)
	service_duration_minute = fields.Selection(selection=mins)
	buffer_hour = fields.Selection(selection=hrs)
	buffer_minute = fields.Selection(selection=mins)

	# Start Operating Timing
	operating_start_hour = fields.Selection(selection=hrs)
	operating_start_minute = fields.Selection(selection=mins)

	# End Operating Timing
	operating_end_hour = fields.Selection(selection=hrs)
	operating_end_minute = fields.Selection(selection=mins)
	
	@api.constrains('type')
	def _check_type(self):
		for record in self:
			if record.type == 'package' and not record.is_package:
				raise ValidationError("If you selected Package as product type,\nyou must also check the above\n \"This is a Package\" checkbox.")
			if record.type == 'book_service' and not record.is_book_service:
				raise ValidationError("If you selected Bookable Service as product type,\nyou must also check the above\n \"This is a Bookable Service\" checkbox.")
			if record.is_package and record.is_book_service:
				raise ValidationError("Product cannot be both Package and Bookable Service.\n Please de-select one.")

	@api.constrains('is_package', 'service', 'quantity', 'validity')
	def _check_package(self):
		for record in self:
			if record.is_package and not record.service:
				raise ValidationError("\"Linked Service\" field cannot be empty. \nPlease fill in the \"Linked Service\" field to link a Service to this Package.")
			if record.is_package and record.quantity == 0:
				raise ValidationError("\"Service Quantity\" field cannot be empty. \nPlease fill in the \"Service Quantity\" field for the number of services in this package.")
			if record.is_package and not record.validity:
				raise ValidationError("\"Validity\" field cannot be empty. \nPlease fill in the \"Validity\" field to indicate the length of the package until expiry.")

	@api.constrains('is_book_service', 'service_duration_hour','service_duration_minute','buffer_hour','buffer_minute')
	def _check_service(self):
		for record in self:
			if record.is_book_service:
				if not record.service_duration_hour or not record.service_duration_minute or not record.buffer_hour or not record.buffer_minute:
					raise ValidationError("Service duration and buffer duration fields cannot be empty. \nPlease fill in all of the required fields to proceed.")

	@api.onchange('is_package')
	@api.depends('is_package')
	def is_package_true(self):
		for each in self:
			if each.is_package:
				each.type = 'package'
			else:
				each.type = 'consu'

	@api.onchange('is_book_service')
	@api.depends('is_book_service')
	def is_book_service_true(self):
		for each in self:
			if each.is_book_service:
				each.type = 'book_service'
			else:
				each.type = 'consu'

	def create_entry(self):
		package = self.env['gv.package']
		package_service = self.env['gv.package.service']

		name = self.name
		service = self.service.id
		quantity = self.quantity
		validity = self.validity.id
		desc = self.description
		
		service_duration_hour = self.service_duration_hour
		service_duration_minute = self.service_duration_minute
		buffer_hour = self.buffer_hour
		buffer_minute = self.buffer_minute
		
		if self.is_package:
			for each in self:
				product = each.id
				vals = {
					'name': name,
					'service': service,
					'quantity': quantity,
					'validity': validity,
					'description': desc,
					}
				created_package = package.create(vals)
				each.package = created_package
		elif self.is_book_service:
			for each in self:
				vals = {'name': name,
					'service_duration_hour': service_duration_hour,
					'service_duration_minute': service_duration_minute,
					'buffer_hour': buffer_hour,
					'buffer_minute': buffer_minute
					}
				each.service = package_service.create(vals)

class add_to_product_product(models.Model):
	_inherit = 'product.product'
	
	@api.onchange('is_package')
	@api.depends('is_package')
	def is_package_true(self):
		for each in self:
			if each.is_package:
				each.type = 'package'
			else:
				each.type = 'consu'

class sale_order_line(models.Model):
	_inherit = 'sale.order.line'
	
	is_package = fields.Boolean(related='product_id.is_package', string='This is a Package')
	package = fields.Many2one(related='product_id.package', string="Package")
	is_book_service = fields.Boolean(related='product_id.is_book_service', string='This is a Bookable Service')
	service = fields.Many2one(related='product_id.service', string="Service")

class sale_order(models.Model):
	_inherit = 'sale.order'

	def create_on_sale_done(self):
		purchase = self.env['purchased.package']
		purchase_service = self.env['purchased.service']
		customer = self.partner_id.id
		date = fields.Date.from_string(self.date_order)
		for each in self.order_line:
			if each.is_package:
				vals = {'customer': customer,
					'package': each.package.id,
					'purchase_date': date,
					}
				purchase.create(vals)
			elif each.is_book_service:
				vals = {'customer': customer,
					'service': each.service.id,
					'purchase_date': date,
					}
				purchase_service.create(vals)
				
				"""

class gv_package_oper(models.Model):
	_name = 'gv.package.oper'
	
	store_name = fields.Many2one('res.company', string="Store Name", required=True)
	branch_name = fields.Char(string="Branch Name", required=True)
	branch_location = fields.Char(string="Branch Location", required=True)
		
	# Hours & Minutes Selection
	
	mins = [
				('01', '01'),('02', '02'),('03', '03'),('04', '04'),('05', '05'),
				('06', '06'),('07', '07'),('08', '08'),('09', '09'),('10', '10'),
				('11', '11'),('12', '12'),('13', '13'),('14', '14'),('15', '15'),
				('16', '16'),('17', '17'),('18', '18'),('19', '19'),('20', '20'),
				('21', '21'),('22', '22'),('23', '23'),('24', '24'),('25', '25'),
				('26', '26'),('27', '27'),('28', '28'),('29', '29'),('30', '30'),
				('31', '31'),('32', '32'),('33', '33'),('34', '34'),('35', '35'),
				('36', '36'),('37', '37'),('38', '38'),('39', '39'),('40', '40'),
				('41', '41'),('42', '42'),('43', '43'),('44', '44'),('45', '45'),
				('46', '46'),('47', '47'),('48', '48'),('49', '49'),('50', '50'),
				('51', '51'),('52', '52'),('53', '53'),('54', '54'),('55', '55'),
				('56', '56'),('57', '57'),('58', '58'),('59', '59'),('00', '00')
				]

	hrs = [
				('01', '01'),('02', '02'),('03', '03'),('04', '04'),('05', '05'),
				('06', '06'),('07', '07'),('08', '08'),('09', '09'),('10', '10'),
				('11', '11'),('12', '12'),('13', '13'),('14', '14'),('15', '15'),
				('16', '16'),('17', '17'),('18', '18'),('19', '19'),('20', '20'),
				('21', '21'),('22', '22'),('23', '23'),('24', '24'),('00', '00')
				]

	# Start Operating Timing

	operating_start_hour = fields.Selection(
				selection=hrs)

	operating_start_minute = fields.Selection(
				selection=mins)

	# End Operating Timing

	operating_end_hour = fields.Selection(
				selection=hrs)

	operating_end_minute = fields.Selection(
				selection=mins)

	start_time = fields.Char(compute='op')
	end_time = fields.Char(compute='opend')
	total_time = fields.Char(compute='ophrs', string="Total Operation Hours")

	# Convert Starting Operating String To Time Format

	@api.depends('operating_start_hour','operating_start_minute')
	@api.onchange('operating_start_hour','operating_start_minute')
	def op(self):
		a=float(self.operating_start_hour)
		b=float(self.operating_start_minute)
		for each in self:
			
			minutes = int(round(a * 60 + b))
			each.start_time = "%02d:%02d" % divmod(minutes, 60)


	# Convert Ending Operating String To Time Format

	@api.depends('operating_end_hour','operating_end_minute')
	@api.onchange('operating_end_hour','operating_end_minute')
	def opend(self):
		c=float(self.operating_end_hour)
		d=float(self.operating_end_minute)
		for each in self:
			
			minutes = int(round(c * 60 + d))
			each.end_time = "%02d:%02d" % divmod(minutes, 60)

	# Calculate Total Operation Hours

	@api.depends('operating_end_hour','operating_end_minute','operating_start_hour','operating_start_minute')
	@api.onchange('operating_end_hour','operating_end_minute','operating_start_hour','operating_start_minute')
	def ophrs(self):
		a=float(self.operating_start_hour)
		b=float(self.operating_start_minute)
		c=float(self.operating_end_hour)
		d=float(self.operating_end_minute)
		for each in self:

			start_minutes = int(round(a * 60 + b))
			end_minutes = int(round(c * 60 + d))
			minutes = end_minutes - start_minutes
			each.total_time = "%02d:%02d" % divmod(minutes, 60)

"""
