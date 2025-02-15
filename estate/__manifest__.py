# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Raj Pavara",
    'category': 'Property',
    'description': """
    Basic Real Estate application
    """,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml', # Maintain the sequance for loading of the data files
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml', 
        'views/estate_property_tag_views.xml', 
        'views/estate_menus.xml',
        'views/res_users_views.xml'
    ]
}
