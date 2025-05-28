{
    "name": "POS Sales Agent",
    "summary": "Adds a sales agent selection button in POS.",
    "version": "0.1",
    "author": "Kashish Singh",
    "website": "https://www.odoo.com",
    "category": "Sales",
    "depends": ["point_of_sale", "hr"],
    "data": [
        "views/pos_order_views.xml",
        "views/pos_sales_agent_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos/static/src/select_sales_agent_button/*.js",
            "pos/static/src/select_sales_agent_button/*.xml",
            "pos/static/src/models/*.js",
            "pos/static/src/control_button/*.js",
        ],
    },
    "license": "LGPL-3",
}
