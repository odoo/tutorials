{
    "name": "ZERO STOCK BLOCKAGE",
    "version": "1.0",
    "summary": "Restrict Sales Order Confirmation if stock is zero",
    "description": "Adds approval mechanism for sales orders with zero stock.",
    "category": "Sales",
    "application": True,
    "depends": ["base", "sale"],
    "data": [
        "views/zero_stock_blockage_views.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
}
