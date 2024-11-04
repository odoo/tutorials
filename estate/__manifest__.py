{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base', 'website'],
    'author': "rame_odoo",
    'category': 'Real Estate/Brokerage',
    'description': """
    Description text
    """,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'reports/estate_property_offers_table.xml',
        'reports/estate_property_reports.xml',
        'reports/estate_property_templates.xml',
        'reports/estate_user_reports.xml',

        'controller/estate_property_controller_view.xml',
        'wizards/add_offer_wizard_view.xml',

        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_inherit_view.xml',
        'views/estate_menus.xml',

        'data/master_data.xml',
    ],
    'demo': ['demo/demo_data.xml'],
    'icon': '/estate/static/logo.png',
    'installable': True,
    'application': True,
}
