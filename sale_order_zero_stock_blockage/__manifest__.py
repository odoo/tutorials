{
    "name": "Sale Order Zero Stock Blockage",
    "description": """
    Zero Stock Blockage is module to prevent order to confirm if product is out of stock.

    But if manager wants then he can aprove that order.
    """,
    "version": "1.0",
    "depends": ['sale_management', 'stock'],
    "author": "danal",
    "category": "Category",
    "license": "LGPL-3",
    "data": [
        "views/sale_order_view.xml",
    ],
    "installable": True,
    'application': False,
}
