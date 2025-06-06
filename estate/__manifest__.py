{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Estate',
    'summary': 'Tutorial module',
    'depends': [
        'website'
    ],
    'data': [
        'data/estate_models.xml',
        'data/estate_property_type.xml',
        'data/estate_property_tag.xml',
        'data/estate_property_offer.xml',
        'data/estate_property.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
        'controllers/estate_controller.xml',
        'security/ir.model.access.csv',
        'security/estate_security.xml',
        'data/estate_tour.xml',
    ],
    "assets": {
        "web.assets_backend": [
            "estate/static/src/js/tour.js",
        ],
    },
    'license': 'OEEL-1',
}
