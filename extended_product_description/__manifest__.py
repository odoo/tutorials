{
    'name': "Extended Product Description",
    'installable': True,
    'license': 'LGPL-3',
    'depends': ['website_sale'],
    'data': [
        'views/product_template_views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'extended_product_description/static/src/**/*.scss',
        ]
    }
}
