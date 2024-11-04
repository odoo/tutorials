{
    'name': "Stock Transport",
    'version': '1.0',
    'depends': ['stock_picking_batch', 'fleet'],
    'author': "Harsh Chaudhari",
    'category': 'Stock Transport',
    'description': """
    Stock Transport description...
    """,
    # data files always loaded at installation
    'data': [
        'secutity/ir.model.access.csv',
        'views/fleet_category_view.xml',
        'views/stock_picking_batch_form_view.xml',
        'views/stock_picking_tree_view.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [],
    'application': False,
    'installable': True,
}
