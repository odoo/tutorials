{
    'name': "Real Estate - Auction",
    'version': '1.0',
    'depends': ['base', 'estate', 'website'],
    'author': "Vaidik Gorasiya - vrgo",
    'description': """
        This module is designed to manage auction for real estate properties.
    """,
    'category': 'Real Estate',
    'data': [
        'views/account_invoice_views.xml',
        'views/estate_property_views.xml',
        'data/ir_cron.xml',
        'views/estate_website.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
