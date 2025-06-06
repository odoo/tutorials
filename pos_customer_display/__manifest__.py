{
     "name": "POS Customer Display",
     "version": "1.0",
     "category": "Point of Sale",
     "description": """
         Enhances the POS Customer Display by showing customer names, order details,
         payment and refund information in a structured format.
     """,
     "author": "Khushi",
     "depends": ["point_of_sale"],
     "installable": True,
     "assets": {
         'point_of_sale.assets_prod': [
             'pos_customer_display/static/src/pos_order.js',
         ],
         'point_of_sale.customer_display_assets': [
             'pos_customer_display/static/src/customer_display/*',
         ],
     },
     "license": "LGPL-3",
}
