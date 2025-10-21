{
    'name': 'Real Estate',
    'summary': 'Manages real estate properties.',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_type_menus.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_tag_menus.xml',
        'views/estate_property_offer_views.xml',
    ],
    'application': True,
    'author': "Odoo",
    'license': 'AGPL-3'
}
