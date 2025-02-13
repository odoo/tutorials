{
    "name": "Real Estate",
    "category": "Real Estate",
    "depends":["base"],
    "data": [
            "security/ir.model.access.csv",
            "views/estate_property_views.xml",
            "views/estate_property_offer.xml",
            "views/estate_property_type.xml",
            "views/estate_property_tag.xml",
            "views/inherited_model.xml",
            "views/estate_menus.xml",
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
