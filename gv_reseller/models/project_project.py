from openerp import models, fields, api, exceptions
import datetime
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

    def update_sale_order_price(self, pricelist_id):
        print '1'
        if self.status=='pending':
            for ol in self.sale_order.order_line:
                # "Other Services" did not have their prices pulled from the DB
                product = self.env['product.product'].with_context(pricelist=pricelist_id).search([("id", "=", ol.product_id.id), ('type', 'not in', ['other', 'consu'])])
                if product and product.type !='other': 
                    ol.price_unit = product.price
#     @api.onchange('status')
#     def automate_project_dates(self):
#         if self.status=='paid':
#             if not self.project_start_date:
#                 self.project_start_date = datetime.date.today()



        