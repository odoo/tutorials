{
    'name': 'Estate',
    'description': """
        It is an application made for users for a purchase and sales
        of there properties and make experience smoother
        """,
    'sequence': 1,
    'depends' : ['base'],
    'category': 'Real Estate/Brokerage',
    'data' : [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_view.xml',
        'views/estate_menus.xml'
        ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
