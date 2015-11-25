from openerp import fields, models, api, exceptions
from openerp.fields import Datetime

class gv_module(models.Model):
    """

    """
    _name = 'gv.module'
    _inherits = {'product.template': 'product_tmpl_id'}
   
    dependencies = fields.Many2many(comodel_name='gv.module',
                            relation='dependencies',
                            column1='id',
                            column2='dependent_id', help='Other modules that this module depends on. This means that selecting the current module will cause the modules in this field to be selected as well.')
    
    dependents = fields.One2many('gv.module', compute="_compute_dependents", help="Other modules that depends on this module. This means that de-selecting the current module will also cause the modules in this field to be de-selected as well.\nThis is a computed field, so make changes on the dependent field of said module if you want to make changes.")
    
    @api.one
    def _compute_dependents(self):
        print str(self.id) + ":" + str(self.dependencies)
        self.dependents = self.env["gv.module"].search([('dependencies', 'in', self.id)])
        
        
#     Type - module/miscellaneous/service
#     Require web design service

    

    
        