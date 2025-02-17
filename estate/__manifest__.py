{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate/Brokerage',
    'summary': 'Manage real estate advertisements and offers',
    'author': 'Khushi',
    'depends': ['base', 'web', 'mail','website'],
    'data': [
        'views/estate_action.xml',
        'views/estate_menus.xml',
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_search_views.xml',
        'data/ir_sequence_data.xml',
        'reports/estate_property_reports.xml',
        'reports/estate_property_template.xml'
    ],
    "demo": [
        "data/estate_property_type_demo.xml",
        "data/estate_property_demo.xml",
        "data/estate_property_offer_demo.xml"
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/description/icon.png',
            'estate/static/src/scss/style.scss'
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
