{
    'name': 'purchase_dicount',
    'description': "Add function for disscount",
    'author': "meet kavathiya",
    'website': "https://www.odoo.com/",
    'category': "Real-estate",
    'version': "0.1",
    'application': True,
    'installable': True,
    'depends': ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_view.xml',
        'wizard/purchase_order_discount_view.xml'
    ],
    'assets': {},
    'license': 'LGPL-3',
}
