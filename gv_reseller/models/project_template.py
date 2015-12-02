from openerp import models, fields, api, exceptions
import re
'''
Created on 27 Nov 2015

@author: gronex
'''

class gv_project_template(models.Model):
    _inherit = 'project.project'

    client_company_name = fields.Char(string="Client Company Name")
    client_business_registration_no = fields.Char(string="Client Biz Registration No")
    client_address_1 = fields.Char(string="Client Address 1")
    client_address_2 = fields.Char(string="Client Address 2")
    client_office_no = fields.Char(string="Client Office No")
    contact_title = fields.Char(string="Contact Title")
    contact_name = fields.Char(string="Contact Name")
    contact_email_address = fields.Char(string="Contact Email Address")

    contact_mobile_no = fields.Char(string="Contact Mobile No")
    remarks = fields.Char(string="Remarks")
    
    @api.constrain('client_office_no', 'contact_email_address', 'contact_mobile_no')
    def validate(self):
        if not self.validate_email(self.contact_email_address):
            raise exceptions.ValidationError('Contact email address is of wrong format.')
        
        if not self.validate_phone(self.client_office_no):
            raise exceptions.ValidationError('Client office number is of wrong format.')
        
        if not self.validate_phone(self.contact_mobile_no):
            raise exceptions.ValidationError('Contact mobile no is of wrong format.')
    
    def validate_email(self, email_address):
        return re.compile('[^@]+@[^@]+\.[^@]+').match(email_address)
    
    def validate_phone(self, phone_number):
        return re.compile('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})').match(phone_number)
        