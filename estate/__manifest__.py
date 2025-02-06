# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Real Estate',
    'version': '1.0',
    'author': 'Ayush',
    'summary': 'Make your real estate management easy!',
    'category': 'Tutorials/RealEstate',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
