from openerp import models, fields, api, exceptions

'''
Created on 27 Nov 2015

@author: gronex
'''

class gv_project_template(models.Model):
    _inherit = 'project.project'

    customer_remarks = fields.Text(string='Customer Remarks')
    admin_remarks = fields.Text(string='Admin Remarks')
    sale_order = fields.Many2one('sale.order', string='Sale Order')
    project_start_date = fields.Date(string='Project Start Date', help="Date in which the project starts, usually after payment is made. Not to be confused with start date. Start Date is the date in which the project is created. As it is part of the core with NOT_NULL constraint enforced, we use it as created date instead.")
    status = fields.Selection([('pending', 'Pending'),
           ('approved','Approved'),
           ('paid','Paid'),
           ('active', 'Active'),
           ('expired','Expired'),
           ('rejected', 'Rejected'),
           ('cancelled','cancelled'),
           ('custom', 'Custom')], string="Status")




        