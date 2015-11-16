from openerp import fields, models, api, exceptions
from openerp.fields import Datetime

class gv_module(models.Model):
    """

    """
    _name = 'gv.module'
    _inherits = {'product.template': 'product_tmpl_id'}
    duration = fields.Integer()
#     Type - module/miscellaneous/service
#     Price
#     Image
#     Title (name)
#     Years
#     Require web design service

    

    
        