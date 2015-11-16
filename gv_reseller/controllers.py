# -*- coding: utf-8 -*-
from openerp import http

# class Reseller(http.Controller):
#     @http.route('/reseller/reseller/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reseller/reseller/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('reseller.listing', {
#             'root': '/reseller/reseller',
#             'objects': http.request.env['reseller.reseller'].search([]),
#         })

#     @http.route('/reseller/reseller/objects/<model("reseller.reseller"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reseller.object', {
#             'object': obj
#         })