{
    'name': "stock_transport",
    'version': '1.0',
    'depends': ['stock_picking_batch', 'fleet', 'stock_delivery'],
    'author': "odoo",
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_model_vehicle_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_picking_batch_views.xml',
    ],
}
