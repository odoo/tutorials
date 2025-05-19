{
    'name': 'estate',
    'license': 'LGPL-3',
    'depends': [
        'website',
    ],
    'data': [
        'models/model_real_estate_property_type.xml',
        'models/model_real_estate_property_tag.xml',
        'models/model_real_estate_property_offer.xml',
        'models/model_real_estate_property.xml',
        'models/estate_property_offer_2.xml',
        'security/ir.model.access.csv',
        'data/estate_tour.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    "assets": {
        "web.assets_backend": [
            "estate/static/src/js/tour.js",
        ],
    },
    "demo": [
        "demo/x_estate.property.type.csv",
    ],
    "installable": True,
    "application": True,
}
