{
    "name": "Real Estate",
    "version": "1.0",
    "sequence": 1,
    "depends": ["base", "mail"],
    "description": """
    This is the estate application being developed as per Tutorial for Technical Training.
    """,
    "category": "Real Estate/Brokerage",
    "installable": True,
    "application": True,
    "license": "LGPL-3",

    "data": [
        'security/estate_security.xml',
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',

        'data/estate.property.type.csv',
    ],

    "demo": [
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
    ],
}
