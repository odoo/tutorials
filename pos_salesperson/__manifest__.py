{
    'name': 'pos_salesperson',
    'version': '1.0',
    'category': 'Point of Sale',
    'website': "https://www.odoo.com/odoo/point-of-sale",
    'summary': 'Add a salesperson selection dropdown in POS',
    'depends': ['point_of_sale', 'hr'],
    'author': 'Abhishek Patel(abpa)',
    'license': 'LGPL-3',
    'data': [
        'views/pos_salesperson_view.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_salesperson/static/src/**/*',
        ],
    },
    'installable': True,
    'application': True,
}
