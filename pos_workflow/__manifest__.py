{
    'name': "Pos Workflow",

    'summary': """
       Module for creating picking from pos order
    """,

    'description': """
        Module for creating picking from pos order
    """,

    'category': 'Sales/Point of Sale',
    'version': '0.1',

    'depends': ['point_of_sale', 'stock_account'],
    'application': True,
    'installable': True,
    'data': [],
    'assets': {'point_of_sale._assets_pos': [
            'pos_workflow/static/src/**/*',
    ], },
    'license': 'AGPL-3'
}
