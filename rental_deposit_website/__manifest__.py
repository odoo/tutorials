{
    'name': 'rental_deposit_website',
    'author': "vikvi",
    'license': 'LGPL-3',
    'depends': ['sale_renting', 'website_sale'],
    "category": "Tutorials",
    'auto_install': True,
    'data': [
        'views/website_cart_overview.xml',
    ],
    "assets": {
        "web.assets_frontend": [
            "rental_deposit_website/static/src/website_rental_deposit_amount.js"
        ],
    },
}
