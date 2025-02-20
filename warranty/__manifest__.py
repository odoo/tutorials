{
    'name': "warranty",
    'version': '18.0',
    'depends': ['sale_management','stock'],
    'author': "Smit",
    'category': 'Sales/Warranty',
    'license' : 'LGPL-3',
    'description': """
        Extend Warranty.
    """,
    'data': [
        'security/ir.model.access.csv',

        'wizard/warranty_add_warranty.xml',

        'views/warranty_views.xml',
        'views/warranty_configuration_menu.xml',
        'views/warranty_configuration_views.xml',
        'views/warranty_sale_order_views.xml',
    ],
    'installable': True,
    'application': True,
}
