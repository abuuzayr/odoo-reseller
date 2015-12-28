from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp import SUPERUSER_ID
from datetime import datetime

import json

class profile(http.Controller):
    
    #Handles the GET request for the route '/profile'
    @http.route(
        ['/profile'],
        auth='user',
        methods=['get'],
        website=True)
    def profile_get(self):
        user = request.env.user
        user_ids = [request.uid]
                       
        if user.is_company:
            company = user
            children = request.env['res.users'].sudo().search([('partner_id.parent_id', '=', user.partner_id.id)])
            for child in children:
                user_ids.append(child.id)
                
        else: 
            company = request.env['res.users'].sudo().search([('partner_id', '=', user.parent_id.id)]) 
            
        


        
        rs_projects = request.env['project.project'].sudo().search([('sale_order.user_id', 'in', user_ids), ('status', 'in', ['pending','approved','paid', 'active'])])
        # calculates the project values for project pie chart
        active_projects = ongoing_projects = 0
        for rs_project in rs_projects:
            if rs_project.status=='active':
                active_projects += 1
                
            else:
                ongoing_projects += 1
      
        total_projects = active_projects + ongoing_projects
             
        if user.is_company:         
            rs_projects = request.env['project.project'].sudo().search([('sale_order.user_id', 'in', user_ids), ('status', 'in', ['approved','paid', 'active'])])
            # calculates the sales figures for the pie chart
            sales = pending_payment = 0.0
            for rs_project in rs_projects:
                if rs_project.status=='approved':
                    pending_payment += rs_project.sale_order.amount_total
                    
                else:
                    sales += rs_project.sale_order.amount_total
            
            total_sales = pending_payment + sales
            return http.request.render('gv_reseller.profile', {
                    'sales': sales,
                    'pending_payment': pending_payment,
                    'total_sales': '{:20,.2f}'.format(total_sales),
                    'active_projects': active_projects,
                    'ongoing_projects': ongoing_projects,
                    'total_projects': total_projects,
                    'user': user,
                    'company': company,
                    'credits': "{:,}".format(company.credits),
                    'company_website': company.website or 'NOT AVAILABLE',
                    'is_admin': user.partner_id.is_company
            })
        
        else: 
            rs_projects = request.env['project.project'].sudo().search([('sale_order.user_id', 'in', user_ids)])
            paid = 0
            unpaid = 0
            for rs_project in rs_projects:
                if rs_project.status == 'pending' or rs_project.status == 'approved' or rs_project.status == 'custom':
                    unpaid += 1
                elif rs_project.status == 'paid' or rs_project.status == 'active' or rs_project.status == 'expired':
                    paid += 1 
            total_payment = paid + unpaid
            return http.request.render('gv_reseller.profile', {
                    'paid': paid,
                    'unpaid': unpaid,
                    'total_payment': total_payment,
                    'active_projects': active_projects,
                    'ongoing_projects': ongoing_projects,
                    'total_projects': total_projects,
                    'user': user,
                    'company': company,
                    'company_website': company.website or 'NOT AVAILABLE',
                    'is_admin': user.partner_id.is_company
            })
                    
        
                