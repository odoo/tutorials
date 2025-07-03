{
    'name': 'Sales Branch',
    'depends': [
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/sale_branch_views.xml',
        'views/sale_order_views.xml',
        'views/sale_branch_menus.xml'
    ],
    'license': 'AGPL-3'
}
