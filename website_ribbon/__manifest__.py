{
    'name': "eCommerce ribbon",
    'category': 'Tutorials/ecommerceRibbon',
    'summary': 'Help users.',
    'version': '1.0',
    'application': True,
    'installable': True,
    'depends': ['base', 'web', 'website_sale', 'stock'],

    'demo': [
        'demo/ribbons.xml'
    ],
    'assets': {
        'website.assets_wysiwyg': [
            'website_ribbon/static/src/js/website_sale.js',
        ],
        'website.backend_assets_all_wysiwyg': [
            'website_ribbon/static/src/js/ribbon.js'
            ]
    },
    'data': [
        'views/product_ribbon_views.xml'
    ],
    'license': 'LGPL-3',
}
