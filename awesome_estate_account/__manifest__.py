{
    'name': 'Estate Account',
    'version': '0.1',
    'category': 'Tutorials',
    'summary': 'Bridge module linking real estate with accounting',
    'description': """
Creates a customer invoice automatically when a property is sold.

This is a link module that depends on both the Estate and Accounting modules.
When a property transitions to 'Sold', this module generates an invoice with
a 6% commission line and administrative fees.
    """,
    'author': 'Patja',
    'license': 'LGPL-3',
    'depends': ['awesome_estate', 'account'],
    'data': [
        'views/awesome_estate_property_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': True,
}
