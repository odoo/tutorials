{
    'name': 'Real Estate',
    'version': '1.0',
    'description': """
    This module handles core property operations, including:
    - Property listings,
    - Handling and tracking of the offers,
    - Property types and tags
    """,
    'depends': ['base'],
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menu.xml',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
