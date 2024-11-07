{
    'name': "Stock Transport",
    'version': '1.0',
    'depends': ['stock_picking_batch', 'fleet'],
    'author': "Ayushmaan (ayve)",
    'category': "Stock Transport",
    'description': """
        Stock Transport Module Ayve
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_category_view.xml',
        'views/stock_picking_view.xml',
        'views/stock_picking_batch_view.xml'
    ],
    'demo': [],
    'application': False,
    'installable': True,
}