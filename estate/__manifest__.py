{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'A real estate management app for listing, selling, and tracking properties.',
    'author': 'Maan Patel',
    'depends': ['base', 'mail', 'website'],
    'data' : [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'views/estate_properties_template.xml',
        'views/estate_properties_details.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'report/estate_property_salesman_report.xml',
    ],
    "demo": [
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
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
