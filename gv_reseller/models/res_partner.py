from openerp import models, fields, api, exceptions

class gv_partner_template(models.Model):
    _inherit = 'res.partner'
    
    business_registration_number = fields.Char(string='Business Registration')
    honorifics = fields.Text(string="Honorifics", help="E.g. Mr/Mrs/Ms/Mdm")
   

class gv_user_template(models.Model):
    _inherit = 'res.users'
    
    credits = fields.Integer(string='Credits', help='Credits')
    
    