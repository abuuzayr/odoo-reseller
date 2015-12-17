from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp import SUPERUSER_ID
from datetime import datetime
import time
import json

class booking(http.Controller):
	@http.route(
		['/shop'],
		auth='user',
		methods=['get'],
		website=True)
	def pricing_shop_redirect(self):
		return request.redirect('/pricing')

	#Handles the GET request for the route '/pricing'
	@http.route(
		['/pricing'],
		auth='user',
		methods=['get'],
		website=True)
	def pricing_get(self, **kw):
		consu_product_templates = request.env['product.template'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('type','=','module')])
		consu_product_product = {}

		misc_product_templates = request.env['product.template'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('type','=','misc')])
		misc_product_product = {}

		other_product_templates = request.env['product.template'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('type','=','other')])
		other_product_product = {}

		optional_product_templates = request.env['product.template'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('type','=','optional')])
		optional_product_product = {}
		optional_product_product_base = {}

		for x in consu_product_templates:
			consu_product_product[x] = request.env['product.product'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('product_tmpl_id', '=', x.id)])
		for x in misc_product_templates:
			misc_product_product[x] = request.env['product.product'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('product_tmpl_id', '=', x.id)])
		for x in other_product_templates:
			other_product_product[x] = request.env['product.product'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('product_tmpl_id', '=', x.id)])
		for x in optional_product_templates:
			optional_product_product[x] = request.env['product.product'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([('product_tmpl_id', '=', x.id)])

		if request.env.user.partner_id.is_company:
			isRSA = True
		else:
			isRSA = False

		product_user_tmpl = request.env.ref('gv_reseller.product_user_tmpl')
		product_user_ppid = request.env['product.product'].with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([("product_tmpl_id", "=", product_user_tmpl.id)])

		return http.request.render('gv_reseller.pricing', {
			'consu_product_templates': consu_product_templates,
			'consu_product_product': consu_product_product,
			'misc_product_templates': misc_product_templates,
			'misc_product_product': misc_product_product,
			'other_product_templates': other_product_templates,
			'other_product_product': other_product_product,
			'optional_product_templates': optional_product_templates,
			'optional_product_product': optional_product_product,
			'users': request.env.user,
			'isRSA': isRSA,
			'per_user_price': product_user_ppid.price,
		})

	@http.route(
		['/pricing/project-details'],
		auth='user',
		methods=['get'],
		website=True)
	def pricing_project(self, **kw):
		if kw['project_id']:
			project = request.env['project.project'].sudo().search([('id','=', kw['project_id'])])[0]

			rs = {}
			rs['project'] = {
				'id': project.id,
				'status': project.status,
				'created_date': project.date_start,
				'project_start_date': project.project_start_date,
				'project_end_date': project.date,
				'total': project.sale_order.amount_total,
				'rs_name': project.user_id.name,
				'rs_contact': project.user_id.phone if project.user_id.phone else '-',
				'rs_email': project.user_id.login,
			}
			rs['sale_order_line'] = []
			for ol in project.sale_order.order_line:
				rs['sale_order_line'].append({
						'ppid': ol.product_id.id,
						'name': ol.name,
						'qty': ol.product_uom_qty,
						'price': ol.price_unit
					})

			contact = project.partner_id.child_ids[0]
			rs['contact'] = {
				'name': contact.name,
				'mobile': contact.mobile,
				'email': contact.email,
				'honorifics': contact.honorifics,
				'remarks': project.customer_remarks
			}
			company = project.partner_id
			rs['company'] = {
				'Company Name': company.name,
				'Business Registration No': company.business_registration_number,
				'Address 1': company.street,
				'Address 2': company.street2,
				'phone': company.phone,
				'email': company.email,
				'Postal Code': company.zip
			}

			return json.dumps(rs)
		else:
			return "204 No-Content"

	#Handles the POST request for the route '/pricing'
	@http.route(
		['/pricing'],
		auth='user',
		methods=['post'],
		website=True)
	def pricing_post(self, **kw):
		sol = request.env['sale.order.line']
		pp = request.env['product.product']
		sollist = []

		m_price = 600.00
		if (len(kw['mppids'].split(',')) < 2):
			m_price = 1200.00

		### get custom prod tpml id
		custom_prod_tpml = request.env.ref('gv_reseller.product_custom_tmpl')
		custom_ppid = pp.search([("product_tmpl_id", "=", custom_prod_tpml.id)])

		product_service_tmpl = request.env.ref('gv_reseller.product_service_tmpl')
		product_service_ppid = pp.search([("product_tmpl_id", "=", product_service_tmpl.id)])	

		product_user_tmpl = request.env.ref('gv_reseller.product_user_tmpl')
		product_user_ppid = pp.with_context(pricelist=request.env.user.partner_id.property_product_pricelist.id).search([("product_tmpl_id", "=", product_user_tmpl.id)])	

		if 'project_id' in kw:			
			project = request.env['project.project'].sudo().search([('id', '=', kw['project_id'])])
			so = project.sale_order
			so.write({'order_line': [(5,)] })
			so = project.sale_order
			if (len(kw['mppids'].split(',')) < 2):
				m_price = 1200.00

			if kw['mppids'] != "":
				for x in kw['mppids'].split(','):
					product = pp.search([('id','=',int(x))])[0]
					solid = sol.sudo().create({
						'name': product.name,
						'product_id': product.id,
						'order_id': so.id,
						'price_unit': m_price
					})
					sollist.append((4,solid.id))

			if kw['oppids'] != "":
				for x in kw['oppids'].split(','):
					product = pp.search([('id','=',int(x))])[0]
					solid = sol.sudo().create({
						'name': product.name,
						'product_id': product.id,
						'order_id': so.id
					})
					sollist.append((4,solid.id))

			if kw['service'] != "":
				for x in kw['service'].split('|'):
					print x
					dat = x.split(';')
					tobj = {
						'name': dat[0],
						'product_id': product_service_ppid.id,
						'order_id': so.id,
						'price_unit':dat[1]
					}
					sollist.append((0,0,tobj))

			sollist.append((0,0, {
					'name': 'Number of Users',
					'product_id': product_user_ppid.id,
					'order_id': so.id,
					'price_unit':product_user_ppid.lst_price,
					'product_uom_qty': kw['user']
				}))

			print sollist
			so.sudo().write({'order_line': sollist})

			project.partner_id.child_ids[0].sudo().write({
				'name': kw['Point of Contact Name'],
				'mobile': kw['Point of Contact Mobile'],
				'email' : kw['Point of Contact Email'],
				'honorifics': kw['Point of Contact Title'], 
				'user_id': request.env.user.id,
				'use_parent_address': True,
				'is_company': False,
			})

			project.partner_id.sudo().write({
				'name': kw['Company Name'], 
				'is_company': True,
				'business_registration_number': kw['Business Registration No'],
				'street': kw['Address 1'],
				'street2': kw['Address 2'],
				'zip': kw['Postal Code'],
				'phone': kw['Company Mobile'],           
				'email' : kw['Company Email'],
				'city': 'Singapore',
			})

			project.sudo().write({
				'customer_remarks': kw['Point of Contact Remarks']
			})

			return '200';

		### CLEARS ANY ORDER LINE
		### WORKFLOW FOR NEW ORDERS
		soc = request.website.sale_get_order(force_create=1)
		soc.write({'order_line': [(5,)] })

		soc = request.website.sale_get_order(force_create=1)
		soid = soc.id

		if kw['mppids'] != "":
			for x in kw['mppids'].split(','):
				product = pp.search([('id','=',int(x))])[0]
				solid = sol.sudo().create({
					'name': product.name,
					'product_id': product.id,
					'order_id': soid,
					'price_unit': m_price
				})
				sollist.append((4,solid.id))

		if kw['oppids'] != "":
			for x in kw['oppids'].split(','):
				product = pp.search([('id','=',int(x))])[0]
				solid = sol.sudo().create({
					'name': product.name,
					'product_id': product.id,
					'order_id': soid
				})
				sollist.append((4,solid.id))

		if kw['service'] != "":
			for x in kw['service'].split('|'):
				print x
				dat = x.split(';')
				tobj = {
					'name': dat[0],
					'product_id': product_service_ppid.id,
					'order_id': soid,
					'price_unit':dat[1]
				}
				sollist.append((0,0,tobj))

		sollist.append((0,0, {
				'name': 'Number of Users',
				'product_id': product_user_ppid.id,
				'order_id': soid,
				'price_unit':product_user_ppid.price,
				'product_uom_qty': kw['user']
			}))

		### Custom product example
		# sollist.append((0,0, {'name':'Custom Order Line', 'product_id':custom_ppid.id, 'order_id':soid, 'price_unit':123.45}))		
		soc.write({
			'order_line': sollist,
			'state': 'draft',
			'pricelist_id': request.env.user.property_product_pricelist.id,
	        'partner_id': request.env.user.partner_id.id,
		})

		contact = request.env['res.partner'].sudo().create({
		    'name': kw['Point of Contact Name'],
		    'mobile': kw['Point of Contact Mobile'],
		    'email' : kw['Point of Contact Email'],
		    'honorifics': kw['Point of Contact Title'], 
		    'user_id': request.env.user.id,
		    'use_parent_address': True,
		    'is_company': False,
		})

		company = request.env['res.partner'].sudo().create({
			'name': kw['Company Name'], 
			'is_company': True,
			'business_registration_number': kw['Business Registration No'],
			'street': kw['Address 1'],
			'street2': kw['Address 2'],
			'zip': kw['Postal Code'],
			'phone': kw['Company Mobile'],           
			'email' : kw['Company Email'],
			'city': 'Singapore',
			'child_ids': [(6, 0, [contact.id])],
			'user_id': request.env.user.id,
		})
		### Create A New Project		
		project = request.env['project.project'].sudo().create({
			'name': kw['Company Name'] + ' - ' + time.strftime("%c"),
			'status': 'pending',
			'sale_order': soc.id,
		    'partner_id': company.id,
			'customer_remarks': kw['Point of Contact Remarks']
		})
		
		request.website.sale_reset()
		return '200'