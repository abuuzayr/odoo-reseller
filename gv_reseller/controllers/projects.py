from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp import SUPERUSER_ID
from datetime import datetime

import json

class projects(http.Controller):
    
    #Handles the GET request for the route '/pricing'
    @http.route(
        ['/projects'],
        auth='user',
        methods=['get'],
        website=True)
    def pricing_get(self):
#         projects = request.env['product.template'].search([('type','=','module')])
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
#         })