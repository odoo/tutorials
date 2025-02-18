# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.  

{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Real Estate/Brokerage',
    'summary': 'Real Estate Advertisement Management',
    'author': 'praj',
    'depends': ['base'],
    'license': 'LGPL-3',
    'data': [
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_user.xml',
        'data/master_data.xml',
        'demo/demo_data.xml'
        ],
    'installable': True,
    'application': True,
}
