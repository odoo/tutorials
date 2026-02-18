{
    'name': 'second_uom',
    'description': "Add Button for second uom",
    'author': "meet kavathiya",
    'website': 'https://www.odoo.com/',
    'category': '',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['point_of_sale'],
    'data': ['views/product_views.xml'],
    'assets': {
        'point_of_sale._assets_pos': [
            'second_uom/static/src/app/**/*.js',
            'second_uom/static/src/app/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}
