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
        'views/estate_property_actions.xml', # Maintain the sequance for loading of the data files
        'views/estate_property_type_actions.xml', 
        'views/estate_property_tag_actions.xml', 
        'views/estate_property_offer_actions.xml', 
        'views/estate_property_menus.xml'
    ]
}
