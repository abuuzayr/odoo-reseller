from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp import SUPERUSER_ID
from datetime import datetime

import json

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
                           'created_date': rs_project.date_start or '-', 
                           'sales_person': rs_project.sale_order.user_id.name or '-',
                           'price': rs_project.sale_order.amount_total or '-',
                           'sales_contact': rs_project.sale_order.user_id.phone or '-',
                           'sales_email': rs_project.sale_order.user_id.email or '-',
                            'customer_company': rs_project.partner_id.name or '-',
                            'customer_contact_name': contact.name or '-',
                            'customer_contact_no': contact.phone or '-',
                            'customer_email': contact.email or '-',
                            'start_date': rs_project.project_start_date or '-', 
                            'expiry_date': rs_project.date or '-',
                            'status': rs_project.status or '-',
                            'approve': rs_project.status == 'pending',
                            'reject': rs_project.status == 'pending' or rs_project.status == 'approved'
                           }
            
            else:
                project = {
                           'id': rs_project.id,
                           'created_date': rs_project.date_start or '-',  
                            'customer_company': rs_project.partner_id.name or '-',
                            'customer_contact_name': contact.name or '-',
                            'customer_contact_no': contact.phone or '-',
                            'customer_email': contact.email or '-',
                            'start_date': rs_project.project_start_date or '-', 
                            'expiry_date': rs_project.date or '-',
                            'status': rs_project.status or '-',
                            'approve': False,
                            'reject': rs_project.status == 'pending'
                           }

            print project
            project_arr.append(project)
             
        
        return http.request.render('gv_reseller.projects', {
            'projects': project_arr,
            'user' : user
       
#         consu_product_product = {}
#  
#         for x in consu_product_templates:
#             consu_product_product[x] = request.env['product.product'].search([('product_tmpl_id', '=', x.id)])
#  
#  
#         return http.request.render('gv_reseller.pricing', {
#             'consu_product_templates': consu_product_templates,
#             'consu_product_product': consu_product_product,
#             'misc_product_templates': misc_product_templates,
#             'misc_product_product': misc_product_product,
#             'other_product_templates': other_product_templates,
#             'other_product_product': other_product_product,
#             'optional_product_templates': optional_product_templates,
#             'optional_product_product': optional_product_product,
#             'user': request.env.user
        })