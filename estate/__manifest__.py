{
    "name": "Real Estate",
    "category": "Real Estate/Brokerage",
    "depends":["base","mail"],
    "data": [
            "security/security.xml",
            "security/ir.model.access.csv",
            "views/estate_property_views.xml",
            "views/estate_property_offer.xml",
            "views/estate_property_type.xml",
            "views/estate_property_tag.xml",
            "views/inherited_model.xml",
            "views/estate_menus.xml",
    ],
    'demo': [
        "demo/estate_property_type_demo.xml",
        "demo/estate_property_tag_demo.xml",
        "demo/estate_property_demo.xml",
        "demo/estate_property_offer_demo.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/description/icon.png',
        ],
    },
    'images': ['static/description/icon.png'],
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}
