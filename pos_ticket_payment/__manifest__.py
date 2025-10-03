{
    "name": "POS Ticket Payment",
    "summary": "Enable direct payment from the ticket screen in POS",
    "description": """
POS Ticket Payment
==================

This module enhances the Point of Sale interface by allowing users to initiate payment directly from the ticket (order) screen.

Key Features:
-------------
- Adds a "Payment" button next to the "Load" button on the ticket screen.
- Clicking "Payment" will load the selected order and navigate to the payment screen.
- Speeds up the checkout process for saved orders.

Ideal for fast-paced retail environments where quick payment access is essential.
""",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": ["point_of_sale"],
    "author": "Dhruvrajsinh Zala (zadh)",
    "version": "0.1",
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_ticket_payment/static/src/app/**/*"
        ]
    }
}
