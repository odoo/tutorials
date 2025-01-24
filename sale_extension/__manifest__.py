{
    'name': 'Sale Extension',
    'version': '1.0',
    'depends': ['base', 'sale', 'sale_management'],
    'author': "Kishan B. Gajera",
    'category': 'Sale/Sale',
    'description': """
        A sample sale extension
    """,

    'application': True,
    'installable': True,

    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'wizard/cost_distribution_wizard.xml',
    ],

    'license':'LGPL-3',
}
