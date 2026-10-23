{
    'name': "Real Estate Advertisement",
    'application': True,
    'category': 'Tutorials',
    'version': '0.1',
    'author': 'Odoo S.A.',
    'license': 'AGPL-3',
    'depends': ['base'],
    'data': [
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'security/ir.access.csv',
     ],
}
