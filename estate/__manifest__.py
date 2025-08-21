{
    'name': 'estate',
    'depends': [
        'website',
    ],
    'data': [
        'models/estate_models.xml',

        'models/fields/estate_property_type.xml',
        'models/fields/estate_property_tag.xml',
        'models/fields/estate_property_offer.xml',
        'models/fields/estate_property.xml',

        'models/estate_server_actions.xml',

        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',

        'views/estate_menus.xml',
        'security/ir.model.access.csv',
        'security/estate.security.xml',

        'data/estate_tour.xml',

    ],

    'demo': [
        'demo/x_estate.property.type.csv',
        'demo/x_estate.property.tag.csv',
        'demo/x_estate.property.xml',
    ],

    "assets": {
        "web.assets_backend": [
            "estate/static/src/js/tour.js",
        ],
    },
    'license': 'LGPL-3',
}
