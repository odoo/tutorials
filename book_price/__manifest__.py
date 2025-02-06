{
    "name": "book price",
    "summary": "Add Pricelist Price (khup)",
    "description": "Add Pricelist Price (khup)",
    "version": "0.1",
    "depends": ["account", "sale"],
    "auto_install": True,
    "license": "AGPL-3",
     "data": [
        'security/ir.model.access.csv',
        'views/account_move_line_views.xml',
        'views/sale_order_views.xml'
    ],
}
