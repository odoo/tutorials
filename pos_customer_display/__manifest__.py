{
    'name': 'POS Customer Display Name',
    'version': '1.0',
    'summary': 'Adding POS customer name on payment screeen',
    'description': """
Showing Customer Diplay Name
============================
This module will show customer name on the customer display.

also will show refund lines septarately under refund subsection.
    """,
    'author': 'Raghav Agiwal',
    'depends': ['point_of_sale'],
    "assets": {
        'point_of_sale.assets_prod': [
            'pos_customer_display/static/src/pos_order.js',
        ],
        'point_of_sale.customer_display_assets': [
            'pos_customer_display/static/src/customer_display/*',
        ],
    },
    'installable': True,
    'license': 'LGPL-3'
}
