from openerp import models, fields, api, exceptions
import re
'''
Created on 27 Nov 2015

@author: gronex
'''

class gv_project_template(models.Model):
    _inherit = 'project.project'

    client_company_name = fields.Char(string="Company Name")
    client_business_registration_no = fields.Char(string="Biz Registration No")
    client_address_1 = fields.Text(string="Address 1")
    client_address_2 = fields.Text(string="Address 2")
    client_office_no = fields.Char(string="Office No")
    contact_title = fields.Char(string="Title")
    contact_name = fields.Char(string="Name")
    contact_email_address = fields.Char(string="Email Address")

    contact_mobile_no = fields.Char(string="Mobile No")
    customer_remarks = fields.Text(string="Customer Remarks")
    admin_remarks = fields.Text(string="Admin Remarks")
    
#     @api.constrain('client_office_no', 'contact_email_address', 'contact_mobile_no')
#     def validate(self):
#         if not self.validate_email(self.contact_email_address):
#             raise exceptions.ValidationError('Contact email address is of wrong format.')
#         
#         if not self.validate_phone(self.client_office_no):
#             raise exceptions.ValidationError('Client office number is of wrong format.')
#         
#         if not self.validate_phone(self.contact_mobile_no):
#             raise exceptions.ValidationError('Contact mobile no is of wrong format.')
#     
#     def validate_email(self, email_address):
#         return re.compile('[^@]+@[^@]+\.[^@]+').match(email_address)
#     
#     def validate_phone(self, phone_number):
#         return re.compile('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})').match(phone_number)
        