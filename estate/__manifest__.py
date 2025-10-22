{
    'name': 'Real Estate',
    'description': 'A tutorial module for real estate management',
    'version': '1.0',
    'depends': ['base'],
    'category': 'Real Estate',
    'summary': 'A basic real estate module',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml'
    ],
    'application': True,
    'author': 'Odoo Sa',
    'license': 'LGPL-3',
}
