{
    'name': "Supplier Bid Price Update",
    'version': '1.0',
    'depends': ['purchase', 'website'],
    'author': "djsh",
    'category': 'Purchase',
    'description': """
Supplier Bid Price Update from portal
""",
    'data': [
        'security/ir.model.access.csv',
        'data/email_templates.xml',
        'views/purchase_views.xml',
        'views/portal_templates.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'supplier_bid_price/static/src/js/update_bid.js',
        ],
    },
    'license': 'LGPL-3',
    'application': True,
}
