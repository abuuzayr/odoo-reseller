from openerp import fields, models, api, exceptions
from openerp.fields import Datetime

class gv_module(models.Model):
    """

    """
    _name = 'gv.module'
    name = fields.Char(string="Title", required=True)
#     Type - module/miscellaneous/service
#     Price
#     Image
#     Title (name)
#     Years
#     Require web design service

    

    
        