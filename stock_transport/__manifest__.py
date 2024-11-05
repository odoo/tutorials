{
    'name': 'Dispatch Management System',
    'version': '1.0',
    'category': 'Transport',
    'summary': 'Extend Fleet Management functionality',
    'description': """
        A module to extend fleet management with additional functionalities.
    """,
    'author': 'rame_odoo',
    'depends': ['fleet', 'delivery_stock_picking_batch', ],
    'data': [

        "security/ir.model.access.csv",
        "views/inherited_vehicle_category_view.xml",
        "views/inherited_stock_picking_batch_view.xml",
        "views/inherited_stock_picking_view.xml",
    ],
    'installable': True,
    'application': False,
}
