{
    "name": "Real Estate",
    "depends": ["base", "mail"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/res_users_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_menus.xml",
    ],
    "demo": [
        "data/estate_property_type_demo.xml",
        "data/estate_property_tag_demo.xml",
        "data/estate_property_demo.xml",
        "data/estate_property_offer_demo.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/src/**',
        ],
    },
    'author': 'Hansil Chapadiya',
    'license': 'LGPL-3'
}
