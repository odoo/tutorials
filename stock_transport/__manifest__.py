{
    'name': "Transport Management System",
    'version': "1.0",
    'summary': "provide tranport facility",
    'description': """
        used for better transport service
    """,
    'author': "Odoo",
    'auto_install': True,
    'data': [
        "views/fleet_vehicle_model_views.xml",
        "views/stock_picking_batch_views.xml",
        "views/stock_picking_views.xml",
    ],
    'assets': {
        
    },
    'license': "LGPL-3",
    'depends': ["stock_picking_batch","fleet","point_of_sale"],
}
