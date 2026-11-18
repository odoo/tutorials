{
    'name': 'Real Estate',
    'version': '1.0',
    'author': 'sadis',
    'license': 'LGPL-3',
    'description': """
    Description text
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
    ],
    'application': True,
}
