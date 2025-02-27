{
    'name': "Redesign Product Catalog",
    'description': """
    Able to see the image on popup in mobile view.
    """,
    'version': '1.0',
    'depends': ['sale_management'],
    'author': "Prince Beladiya",
    'license': 'LGPL-3',
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'redesign_product_catalog/static/src/**/*',
        ],
    },
    'data': [
        'views/product_view.xml'
    ]
}
