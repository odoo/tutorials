{
    'name': "Real Estate",
    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Real Estate/Brokerage',
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_res_users_views.xml',
        'views/estate_menus.xml',
        'data/property_type_data.xml',
        'data/property_data.xml',
        'data/property_offer_data.xml'
    ],
    'license': 'AGPL-3'
}
