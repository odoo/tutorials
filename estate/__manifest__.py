{
    'name': 'E-State!',
    'summary': 'Manage real estate advertisements',
    'description': """
        Manage advertisements and offers for different real estate properties as part of the "Sever framework 101" tutorial
    """,
    'author': 'Odoo',
    'website': 'https://www.odoo.com',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'AGPL-3',
}
