{
    'name': 'Distribute Cost Price',
    'depends': [
        'sale_management'
    ],
    'data': [

        'security/ir.model.access.csv',

        'wizard/order_line_wizard.xml',

        'views/sale_oder_inherit_view.xml',

    ],
    'installable': True,
    'license': 'LGPL-3',
}
