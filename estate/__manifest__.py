{
    'name': "Real Estate",
    'version': '1.03',
    'author': "Valam",
    'category': 'Estate category',
    'description': """
    Description text
    """,
    'license': 'LGPL-3',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
    ],
    'demo': [
        'demo/estate.property.type.csv',
        'demo/estate_property.xml',
        'demo/estate_property_offer.xml',
    ],
    'application': True,
}
