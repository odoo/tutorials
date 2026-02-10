{
    'name': "Real Estate",
    'application': True,
    'installable': True,
    'category': "Real Estate/Brokerage",
    'version': '1.0',
    'summary': "The Real Estate Advertisement",
    "depends": [
        "base",
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'author': "rencelotm",
    'license': "AGPL-3"
}