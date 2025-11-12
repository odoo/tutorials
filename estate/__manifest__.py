{
    'name': "Estate",
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['base'],
    'author': "Kalpan Desai",
    'category': 'Estate/sales',
    'description': """
        Module specifically designed for real estate business case.
    """,
    'installable': True,
    'application': True,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_res_user_views.xml',
        'views/estate_menus.xml',
        'report/estate_reports.xml',
        'report/estate_report_views.xml',
    ],
    'demo': [
        'data/estate_demo.xml',
        # 'demo/estate.property.type.csv',
        # 'demo/estate.property.xml',
    ],

}
