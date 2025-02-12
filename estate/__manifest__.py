{
    "name": "Estate",
    "author": "Rohit Kalsariya",
    "license": "LGPL-3",
    "application": True,
    "depends": ["base"],
    'category': 'Real Estate/Brokerage',
    "description": """ 
    The Real Estate Advertisement module.
    """,
    "data": [
        "security/estate_security.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
        "security/ir.model.access.csv",
        'views/res_users_views.xml',
    ],
}
