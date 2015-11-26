from openerp import models, fields, api, exceptions

class gv_product_template(models.Model):
	_inherit = 'product.template'

	type = fields.Selection(selection_add=[
		('misc', 'Miscellaneous'),
		('other', 'Other Services'),
		('optional', 'Optional')
	])
	
	dependent_modules = fields.Many2many('product.template')