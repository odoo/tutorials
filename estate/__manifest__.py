{
    'name': 'Real Estate',
    'summary': """
        Starting module for "Server framework 101"
    """,
    'description': """
        Starting module for "Server framework 101"
    """,
    'author': 'Odoo',
    'website': 'https://www.odoo.com',
    'license': 'LGPL-3',
    'category': 'Tutorials/Real Estate',
    'version': '0.1',
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
    ],
    'depends': ['base'],
}
