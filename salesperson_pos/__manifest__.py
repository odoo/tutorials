{
    'name': "Salesperson in Pos",
    'summary': "Add Salesperson to POS orders",
    'description': """
        This module will add a button in the POS dashboard to assign a salesperson to respective orders.
    """,
    'author': "Devmitra Sharma",
    'depends': ['point_of_sale','hr'],
    'data': [
        "views/pos_form_view.xml",
        "views/hr_employee_form.xml",
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'salesperson_pos/static/src/**/*'
        ],
        'web.assets_backend': [
            'salesperson_pos/static/src/**/*.scss',
        ],
    },
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
}
