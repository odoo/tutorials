{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base', 'mail', 'website'],
    'category': 'Real Estate/Brokerage',
    'author': "Soham Zadafiya [soza]",
    'description': """
        Description text
    """,
    'application': True,
    'data' : [
        'security/estate_groups.xml',
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'wizard/estate_wizard_view.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
        'views/res_users_view.xml',
        'views/estate_website_template.xml',
        'data/estate_property_data.xml',
    ],
    'demo' : [
        'demo/estate_property_demo.xml'
    ],
    'license': 'LGPL-3'
}
