from openerp import models, fields, api, exceptions
import re
'''
Created on 27 Nov 2015

@author: gronex
'''

class gv_project_template(models.Model):
    _inherit = 'project.project'

    client_business_registration_no = fields.Char(string='Biz Registration No')
    customer_remarks = fields.Text(string='Customer Remarks')
    admin_remarks = fields.Text(string='Admin Remarks')
    sale_order = fields.Many2one('sale.order', string='Sale Order')




class gv_partner_template(models.Model):
    _inherit = 'res.partner'
    
    business_registration_number = fields.Char(string='Business Registration')