{
    'name': "stock_transport",
    'depends': ['stock_picking_batch', 'fleet'],
    'author': "sahm@odoo.com",
    'description': "This is my stock_transport module.",
    'data': [
        'security/stock_transport_security.xml',
        'security/ir.model.access.csv',
        'views/stock_picking_batch_views.xml',
        'views/fleet_vehicle_model_views.xml',
        'views/stock_picking_views.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'application': False,
    'auto_install': False
}
