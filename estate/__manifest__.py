# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.  

{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Real Estate Advertisement Management',
    'author': 'praj',
    'depends': ['base'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/inherited_model.xml'
        ],
    'installable': True,
    'application': True,
}
