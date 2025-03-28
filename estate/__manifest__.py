{
    'name': 'Real Estate',
    'version': '1.0',
    'author': 'Odoo',
    'category': 'Estate',
    'summary': 'Real Estate properties manager',
    'description': """
The real estate application hels users to manage their real estate properties by registering data about them including tags, types and salesperson.
The application also allows to register offers on a property form, and track the state of a given property.
    """,
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
    ],
    'license': 'LGPL-3'
}
