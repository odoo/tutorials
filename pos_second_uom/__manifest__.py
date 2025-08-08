{
    'name': 'POS Second UOM',
    'version': '1.0',
    'summary': 'Allows products to have a second unit of measure in POS',
    'description': """
        Adds the ability to set and use a second unit of measure for products in the Point of Sale.
        This is useful for businesses that sell products in multiple units.
        The second UOM is displayed and managed directly within the POS interface for easier sales handling.
    """,
    'author': 'Raghav Agiwal',
    'depends': ['point_of_sale'],
    'data': [
        'views/product_template_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_second_uom/static/src/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3'
}
