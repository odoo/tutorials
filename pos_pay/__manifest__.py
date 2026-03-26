{
    "name": "Instant Pay",
    "summary": """
    Pay directly from Ticked Screen
    """,
    "description": """
        Pay directly from Ticked Screen
    """,
    "author": "Odoo",
    "website": "https://www.odoo.com/",
    "category": "Tutorials",
    "version": "0.1",
    "application": True,
    "installable": True,
    "depends": ["base", "point_of_sale"],
    "data": [],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_pay/static/src/app/screens/ticket_screen.js",
            "pos_pay/static/src/app/screens/ticket_screen.xml",
        ],
    },
    "license": "AGPL-3",
}
