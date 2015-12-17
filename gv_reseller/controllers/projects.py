from openerp.addons.web import http
from openerp.addons.web.http import request
from dateutil import parser


class projects(http.Controller):
    
    #Handles the GET request for the route '/projects'
    @http.route(
        ['/projects'],
        auth='user',
        methods=['get'],
        website=True)
    def projects_get(self):
        user = request.env.user
        user_ids = []
        user_ids.append(request.uid)

        if user.child_ids:
#             child_ids = []
#             for child in user.child_ids:
#                 child_ids.append(child.id)
#             children = request.env['res.user'].sudo().search([('partner_id', 'in', child_ids)])
            children = request.env['res.users'].sudo().search([('partner_id.parent_id', '=', user.partner_id.id)])
            for child in children:
                user_ids.append(child.id)
        
        user = {
                'id': user.id,
                'is_admin': user.partner_id.is_company
                }
        
        rs_projects = request.env['project.project'].sudo().search([('sale_order.user_id', 'in', user_ids)]) #WHERE USER IS CUSTOMER OF PROJECT
        
        project_arr = []
        
        for rs_project in rs_projects:
            
            contact = rs_project.partner_id.child_ids[0]
            
            if request.env.user.partner_id.is_company:
                project = {
                           'id': rs_project.id,
                           'created_date': self.format_date(rs_project.date_start), 
                           'sales_person': rs_project.sale_order.user_id.name or '-',
                           'price': rs_project.sale_order.amount_total or '0.00',
                           'sales_contact': rs_project.sale_order.user_id.phone or '-',
                           'sales_email': rs_project.sale_order.user_id.email or '-',
                            'customer_company': rs_project.partner_id.name or '-',
                            'customer_contact_name': contact.name or '-',
                            'customer_contact_no': contact.mobile or '-',
                            'customer_email': contact.email or '-',
                            'start_date': self.format_date(rs_project.project_start_date), 
                            'expiry_date': self.format_date(rs_project.date),
                            'status': rs_project.status or '-',
                            'approve': rs_project.status == 'pending',
                            'reject': rs_project.status == 'pending' or rs_project.status == 'approved'
                           }
            
            else:
                project = {
                           'id': rs_project.id,
                           'created_date': self.format_date(rs_project.date_start),  
                            'customer_company': rs_project.partner_id.name or '-',
                            'customer_contact_name': contact.name or '-',
                            'customer_contact_no': contact.mobile or '-',
                            'customer_email': contact.email or '-',
                            'start_date': self.format_date(rs_project.project_start_date), 
                            'expiry_date': self.format_date(rs_project.date),
                            'status': rs_project.status or '-',
                            'approve': False,
                            'reject': rs_project.status == 'pending'
                           }
            project_arr.append(project)
             
        return http.request.render('gv_reseller.projects', {
            'projects': project_arr,
            'user' : user
        })
        
    @http.route(
        ['/custom-project'],
        auth='user',
        methods=['get'],
        website=True)
    def custom_project(self, **kwargs):
        if 'project_id' in kwargs:
            rs_project = request.env['project.project'].sudo().search([('id', '=', kwargs['project_id'])])
            if rs_project: 
                contact = rs_project.partner_id.child_ids[0]
                company = rs_project.partner_id
                project = {
                           'id': rs_project.id,
                            'company_name': company.name or '',
                            'business_registration_no': company.business_registration_number or '',
                            'customer_address_line_1': company.street or '',
                            'customer_address_line_2': company.street2 or '',
                            'office_no': company.phone,
                            'postal_code': company.zip,
                            
                            'name': contact.name or '',
                            'email_address': contact.email or '',
                            'title': contact.honorifics or '', 
                            'contact_no': contact.mobile or '',
                            
                            'remarks': rs_project.customer_remarks,
                           }
                return http.request.render('gv_reseller.custom-project', {
                    'project': project,
                    'user' : request.env.user
                })
        
        project = {
                       'id': '0',
                        'company_name': '',
                        'business_registration_no': '',
                        'customer_address_line_1': '',
                        'customer_address_line_2': '',
                        'office_no': '',
                        'postal_code': '',
                        
                        'name': '',
                        'email_address': '',
                        'title': '', 
                        'contact_no': '',
                        
                        'remarks': '',
                       }       
        return http.request.render('gv_reseller.custom-project', {
                'project': project,
                'user' : request.env.user
            })

    @http.route(
        ['/custom-project/create'],
        auth='user',
        methods=['get'],
        website=True)
    def create_custom_project(self, **kwargs):
        if kwargs['project_id'] == '0' :
            contact_val = {
                'name': kwargs['name'],
                'mobile': kwargs['contact-no'],
                'email' : kwargs['email-address'],
                'honorifics': kwargs['title'], 
                'user_id': request.env.user.id,
                'use_parent_address': True,
                'is_company': False,
                           }
            contact = request.env['res.partner'].sudo().create(contact_val)
            company_val = {
                   'name': kwargs['company-name'], 
                   'is_company': True,
                    'business_registration_number': kwargs['business-registration-no'], 
                    'street': kwargs['company-address-1'],
                    'street2': kwargs['company-address-2'],
                    'zip': kwargs['postal-code'],
                    'phone': kwargs['office-no'],
                    'email' : kwargs['email-address'],
                    'city': 'Singapore',
                    'child_ids': [(6, 0, [contact.id])],
                    'user_id': request.env.user.id,
                    }
            company = request.env['res.partner'].sudo().create(company_val)
            sale_order_val = {
                    'user_id': request.env.user.id,
                    'pricelist_id': request.env.user.property_product_pricelist.id,
                    'partner_id': request.env.user.partner_id.id,
                              }
            sale_order = request.env['sale.order'].sudo().create(sale_order_val)
            project_val = {
                   'name': kwargs['company-name'], 
                   'status': 'custom',
                   'customer_remarks': kwargs['remarks'],
                   'partner_id': company.id,
                   'sale_order': sale_order.id,
                   }
            project = request.env['project.project'].sudo().create(project_val)
            return request.redirect('/custom-project'+'?project_id='+str(project.id))
            

    @http.route(
        ['/projects/approve-project'],
        auth='user',
        methods=['get'],
        website=True)
    def approve_project(self, **kwargs):
        project = request.env['project.project'].sudo().search([('id', '=', kwargs['project_id'])])
        if project and request.env.user.partner_id.is_company:
            if project.status == 'pending':
                project.status = 'approved'
            
    @http.route(
        ['/projects/reject-project'],
        auth='user',
        methods=['get'],
        website=True)
    def reject_project(self, **kwargs):
        project = request.env['project.project'].sudo().search([('id', '=', kwargs['project_id'])])
        if project:
            if project.status == 'pending' or (project.status == 'approved' and request.env.user.partner_id.is_company):
                project.status = 'rejected'

    @http.route(
        ['/project-details'],
        auth='user',
        methods=['get'],
        website=True)
    def get_project_details(self, **kwargs):
        if 'project_id' in kwargs:
            project = request.env['project.project'].sudo().search([('id', '=', kwargs['project_id'])])
            if project.status == 'custom': 
                return request.redirect('/custom-project'+'?project_id='+kwargs['project_id'])
            else:
                return request.redirect('/pricing'+'?project_id='+kwargs['project_id'])

    def format_date(self, date):
        if date:
            my_date = parser.parse(date)
            return my_date.strftime("%d/%m/%Y")
        return '-'
    