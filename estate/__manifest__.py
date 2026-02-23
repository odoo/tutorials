{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base'],
    'author': 'viwar-odoo',
    'category': 'real estate',
    'description': "real estate App.",
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml'
        
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'website': 'https://odoo.com',
}
