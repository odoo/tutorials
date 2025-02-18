# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    'website': 'https://www.odoo.com/page/estate',
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
        
        
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'application': True,
    'installable': True
}