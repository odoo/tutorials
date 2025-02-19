{
    'name': 'RealEstate',
    'version': '1.0',
    'author': 'Odoo S.A.',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'icon': '/estate/static/real_estate.png',
    'installable': True,
    'application': True,
    'auto_install': False,
    'category': 'Tools',
    'summary': 'Managing real estate properties efficiently',
    'license': 'LGPL-3',
}
