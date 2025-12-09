{
    'name': 'Rental App',
    'category': '',
    'description': """This module is  rental app module""",
    'depends': ['sale_renting', 'website_sale_renting'],
    'data': [
        "views/res_config_settings_views.xml",
        "views/product_template_views.xml",
        "views/templates.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'rental_deposit/static/src/js/rental_deposit.js',
        ],
    },
    'application': True,
    'license': 'OEEL-1',
    "sequence": 1,
}
