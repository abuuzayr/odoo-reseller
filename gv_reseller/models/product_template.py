from openerp import models, fields, api, exceptions

class gv_product_template(models.Model):
	_inherit = 'product.template'

	type = fields.Selection(selection_add=[
		('module', 'Modules'),
		('misc', 'Miscellaneous Modules'),
		('other', 'Other Services'),
		('optional', 'Optional Services'),
		('user', 'Users')
	])
	
	dependencies = fields.Many2many(comodel_name='product.template',
							relation='dependencies',
							column1='id',
							column2='dependent_id', help='Other modules that this module depends on. This means that selecting the current module will cause the modules in this field to be selected as well.')

	dependents = fields.One2many('product.template', compute="_compute_dependents", help="Other modules that depends on this module. This means that de-selecting the current module will also cause the modules in this field to be de-selected as well.\nThis is a computed field, so make changes on the dependent field of said module if you want to make changes.")
	other_services = fields.One2many('product.template', 'id', help='Other services that should be made available when this module is selected')
	duration = fields.Integer(help="Number of hours for a particular service to take")
	
	@api.one
	def _compute_dependents(self):
		if self.id:
			self.dependents = self.env["product.template"].search([('dependencies', 'in', self.id)])
		
	