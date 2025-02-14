{
    'name': 'Estate',
    'description': """
        It is a Real Estate application made for users for a comfortable purchase
        and sales of there properties
        """,
    'sequence': 1,
    'category': 'Real Estate/Brokerage',
    'depends' : ['base','mail'],
    'data' : [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_offer.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml'
        ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
