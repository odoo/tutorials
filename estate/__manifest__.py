{
    "name": "Real Estate",
    "version": "1.0",
    "sequence": 1,
    "depends": ["base"],
    "description": """
    This is the estate application being developed as per Tutorial for Technical Training.
    """,
    "installable": True,
    "application": True,
    "license": "LGPL-3",

    "data": [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml',
        'views/estate_menu_views.xml',
    ]
}
