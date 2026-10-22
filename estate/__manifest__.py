{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Samuel (sawer)",
    'category': 'Tutorials',
    'description': """
    Description text
    """,
    'data': [
        'security/ir.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml',
        'report/res_users_reports.xml',
        'report/res_users_templates.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'license': "LGPL-3"
}
