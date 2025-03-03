{
    'name': "Rental Deposit",
    'version': '1.0',
    'depends': ['website_sale_renting'],
    'author': "ppch",
    'category': 'Category',
    'description': """
    Rental Deposit is configured and it will be added as deposit product whenever any product
    which has deposit required will be true and it will work in both frontend and backend
    """,
    'license': "LGPL-3",
    'data': [
        'views/res_config_settings_views.xml',
        'views/product_template_views.xml',
        'views/website_rent_template.xml'
    ],
    'installable': True,
}
