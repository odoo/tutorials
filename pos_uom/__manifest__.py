{
    'name': "POS UOM Conversion",
    'summary': """
        Module for Adding Second Uom for POS
    """,
    'description': """
        Module for Adding Second Uom for POS
    """,
    'category': 'Sales/Point of Sale',
    'version': '0.1',
    'application': True,
    'installable': True,
    'data': ['views/product_template_form_view.xml'],
    'depends': ['point_of_sale', 'web'],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_uom/static/src/**/*',
        ],
        'web.assets_tests': [
            'pos_uom/static/tests/tours/**/*',
        ],
    },
    'license': 'AGPL-3'
}
