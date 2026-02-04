{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base', 'mail'],
    'author': 'Dhrudeep',
    'description': """
        This module provides functionality to manage real estate properties.
        """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_maintenance_requests_view.xml',
        'views/estate_investor_profile_view.xml',
        'views/estate_res_users_view.xml',
        'views/estate_menus.xml',
        'data/estate_mail_template.xml'
    ],
    'category': 'Tutorial',
    'license': 'LGPL-3',
    'application': True,
}
