{
    'name': 'Estate',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Odoo S.A.',
    'application': True,
    'installable': True,
    'category': '',
    'description': '',
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml'
    ]
}
