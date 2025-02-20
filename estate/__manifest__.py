{
    'name': "estate",
    'depends': ['base','mail','website'],
    'application': True,
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tags_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/master_data.xml',
        'report/estate_report_views.xml',
        'report/estate_reports.xml',
        'views/property_templates.xml'
    ],
    "demo": [
        "demo/estate_demo.xml"
    ],
    'test': [
        'tests/test_estate',  
    ],
    'category':'Real Estate/Brokerage',
    'license': 'LGPL-3'  
}
