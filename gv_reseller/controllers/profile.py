from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp import SUPERUSER_ID
from datetime import datetime

import json

class profile(http.Controller):
    
    #Handles the GET request for the route '/projects'
    @http.route(
        ['/profile'],
        auth='user',
        methods=['get'],
        website=True)
    def projects_get(self):
        user = request.env.user
        user_ids = [request.uid]
                       
        if user.is_company:
            company = user
            children = request.env['res.users'].sudo().search([('partner_id.parent_id', '=', user.partner_id.id)])
            for child in children:
                user_ids.append(child.id)
        else: 
            company = user.parent_id
        
        
        #get user price
        product_user = request.env['product.template'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('type','=','user')])
        if product_user: 
            user_price = product_user.price
        else:
            user_price = 50.00
        
        rs_projects = request.env['project.project'].sudo().search([('sale_order.user_id', 'in', user_ids), ('status', 'in', ['approved','paid', 'active'])])
     
        
        sales = pending_payment = 0.0
        for rs_project in rs_projects:
            if rs_project.status=='approved':
                pending_payment += rs_project.sale_order.amount_total
                
            else:
                sales += rs_project.sale_order.amount_total
        
        total_sales = pending_payment + sales
        
        rs_projects = request.env['project.project'].sudo().search([('sale_order.user_id', 'in', user_ids), ('status', 'in', ['pending','approved','paid', 'active'])])
        
        active_projects = ongoing_projects = 0
        for rs_project in rs_projects:
            if rs_project.status=='active':
                active_projects += 1
                
            else:
                ongoing_projects += 1
      
        total_projects = active_projects + ongoing_projects
        
         
        #
        return http.request.render('gv_reseller.profile', {
                'user_price': user_price,
                'sales': sales,
                'pending_payment': pending_payment,
                'total_sales': '{:20,.2f}'.format(total_sales),
                'active_projects': active_projects,
                'ongoing_projects': ongoing_projects,
                'total_projects': total_projects,
                'user': user,
                'company': company,
                'is_admin': user.partner_id.is_company
            })
        # sales, pending_payment, total_sales, active_projects, ongoing_projects, expired_projects
        
                