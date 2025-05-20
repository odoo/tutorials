{
    'name': "Product Tutorial",
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/res_groups.xml',
        'security/res_users.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',

        'data/product_data.xml',

        'views/category_views.xml',
        'views/product_views.xml',
        'views/menus.xml',
    ],
    'application': True,
}
