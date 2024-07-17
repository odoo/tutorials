{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Vansh",
    'category': 'estate',
    'description': """Find Your property Here""",
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_user_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_setting_views.xml',
        'views/estate_menus.xml',
        "data/estate.property.type.csv",
    ],
    "demo": [
        "demo/demo_estate_property.xml",
    ],
    'images': ['static/description/estate.png'],
    'application': True,
    'installable': True,
    'license': "AGPL-3"
}
