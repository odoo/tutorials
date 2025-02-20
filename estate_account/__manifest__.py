{
    'name' : "Real Estate Account",

    'summary' : "A module integrating real estate management with accounting in Odoo.",

    'description': """This module enhances real estate operations by seamlessly integrating with Odoo's accounting system. It automates financial transactions, manages invoices, and ensures accurate bookkeeping for property sales and rentals.""",

    'author': "Krunal Gelot",
    'website': "https://www.odoo.com",

    'category': 'Tutorials',
    'version': '0.1',

    'depends': ['estate', 'account'],
    'application': True,
    'installable': True,

    'data':[
        'report/estate_property_account_template.xml'
    ],

    'license': 'AGPL-3'
}
