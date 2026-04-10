{
    'name': "Estate",
    'version': '0.1',
    'summary': "Real Estate Advertisement",
    'description': """
        This module allows you to manage real estate advertisements, including
        properties, agents, and customer inquiries.
    """,
    'author': "aykhu",
    'license': 'LGPL-3',
    'website': "https://www.odoo.com/app/estate",
    'category': 'Tutorials',
    'application': True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml'
    ],
}
