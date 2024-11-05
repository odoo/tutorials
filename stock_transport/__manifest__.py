{
    'name': "Stock Transport",
    'version': '1.0',
    'depends': ['stock_picking_batch', 'fleet', 'web_gantt'],
    'author': "Rajat",
    'description': """ Description text""",
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_vehicle_model_views_inherited.xml',
        'views/stock_picking_batch_view_inherited.xml',
        'views/stock_picking_inherited.xml',
        'views/stock_picking_graph_views.xml'
    ],
    'application': False,
    'installable': True
}
