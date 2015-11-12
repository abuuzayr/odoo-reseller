# -*- coding: utf-8 -*-
{
    'name': "Reseller",

    'summary': """
        Reseller Portal Module
	""",

    'description': """
        Key focus for Gronex Reseller Portal is for convenience and easy communication between resellers, ops and It implementation team. Its to minimize miscommunication and allow sales teams to focus on doing sales while making it an easy process to lay out to ops on the incoming projects.
        
        Functions:
        Allow resellers to download collaterals
        To provide instant access to resellers for all necessary tools to do their sales smoothly
        Allow resellers to send order to ops in 1 simple step
        To provide comprehensive information for resellers for Product Information
        To adhere to assist Resellers’ help request electronically
        To allow bookkeeping for resellers to refer for history, past projects and account details
        Allow access to demo according to permission levels for resellers

	""",

    'author': "Groventure Holdings",
    'website': "http://www.groventure.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
		'mail',
		'product',
        'hr',
	],

    # always loaded
    'data': [
#        'security/security.xml',
#        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo.xml',
    #],
	'installable': True,
	'application': True,
	'auto_install': False,
}
