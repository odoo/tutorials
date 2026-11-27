{
    'name': 'estate_module',
    'version': '1.0',
    'summary': 'Sales real estates',
    'author': 'lobas',
    'license': 'LGPL-3',
    'depends': ['base', 'base_import_module', 'website', 'web_tour'],
    'data': [
        'models/estate_property_type.xml',
        'models/estate_property_tag.xml',
        'models/estate_property.xml',
        'models/estate_property_offer.xml',
        'security/ir.access.csv',
        'actions/estate_api.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'data/new_estate_tour.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'estate_module/static/src/js/tour.js',
        ],
    },
}
