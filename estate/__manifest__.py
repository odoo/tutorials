{
    'name': "Real Estate",
    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_menus.xml',
    ],
    'license': 'AGPL-3'
}
