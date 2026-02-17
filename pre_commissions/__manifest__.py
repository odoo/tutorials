{
    'name': "Sale Commission",
    'author': "Kunj Koradiya",
    'description': "This is the description",
    'license': "LGPL-3",
    'depends': ['base', 'account', 'sale_management'],
    'auto_install': True,
    'data': [
        'security/ir.model.access.csv',
        'views/commision_rule.xml',
        'views/sale_commission.xml',
        'views/menus.xml'
    ],
    'demo': [
        'data/demo.xml'
    ]
}
