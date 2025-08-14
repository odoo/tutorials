{
    'name': 'Estate',
    'summary': "Module to manage properties",
    'description': """
This module is used to manage any type of properties and also to manage the selling pipeline for each property
    """,
    'author': 'Odoo',
    'version': '1.0',
    'depends': ['base'],
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml']
}
