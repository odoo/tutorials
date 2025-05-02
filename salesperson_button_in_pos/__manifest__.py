{
    'name': 'Salesperson button in POS',
    'version': '1.0',
    'summary': 'Adding a salesperson button in pos',
    'description': """
        Adding salesperson button in pos
    """,
    'author': 'Raghav Agiwal',
    'depends': ['point_of_sale', 'hr'],
    'data': [
        'views/pos_order_view.xml',
        'views/employee_form_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'salesperson_button_in_pos/static/src/app/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
