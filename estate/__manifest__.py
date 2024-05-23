{
    'name': "Real Estate",
    'summary': """
        Real Estate app to discover Odoo
    """,
    'description': """
        Real Estate app to discover Odoo
    """,
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/inherited_res_users_views.xml',
    ],
    'license': 'AGPL-3'
}
