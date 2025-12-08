{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'depends': ['base'],
    'author': 'snrav-odoo',
    'license': 'LGPL-3',
    'description': 'Real estate purchase & sales',
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_menu.xml',
        'security/ir.model.access.csv'
        ],
    'application': True,
}
