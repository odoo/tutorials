{
    'name': 'Real Estate',
    'version': '1.0',
    'author': 'sadis',
    'license': 'LGPL-3',
    'description': """
    Real Estate Application
    """,
    'category': 'Tutorials',
    'depends': [
        'base',
        'sales_team',
        'contacts',
    ],
    'data': [
        'security/ir.access.csv',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menu_views.xml',
        'views/res_users_view.xml',
    ],
    'application': True,
}
