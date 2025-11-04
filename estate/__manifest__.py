{
    'name': "estate app",
    'summary': "estate module",
    'description': "Estate module for buying and selling properties. Users can buy/sell properties via estate agents",
    'author': "Odoo",
    'category': 'Real Estate/Brokerage',
    'version': '1.0',
    'depends': ['base','mail', 'web', 'website'],
    'data':[
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        "views/estate_users_views.xml",
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_details_template.xml',
        'views/estate_property_list_template.xml',
        #'views/estate_property_make_offer_template.xml',
        'views/estate_menus.xml',
        'data/estate_property_type_data.xml',
        'report/estate_reports.xml',
        'report/estate_report_views.xml',
    ],
    'demo':[
        'data/estate_property_demo.xml',
        'data/estate_property_offer_demo.xml'
    ],
    'application': True,
    'installable': True,
    'license': 'AGPL-3'
}

