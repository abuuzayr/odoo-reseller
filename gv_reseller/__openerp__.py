# -*- coding: utf-8 -*-
{
    'name': "GV Reseller",

    'summary': """
        Key focus for Gronex Reseller Portal is for convenience and easy communication between resellers, ops and It implementation team. Its to minimize miscommunication and allow sales teams to focus on doing sales while making it an easy process to lay out to ops on the incoming projects.
    """,

    'description': """

    """,

    'author': "Groventure Holdings",
    'website': "http://www.groventure.com.sg",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        'security/gv_reseller_security.xml',
        'templates.xml',
        'module.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}