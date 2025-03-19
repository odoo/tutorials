{
    'name': "Warranty Extension",
    'version': '18.0',
    'depends': ['sale_management','stock'],
    'author': "Rahul",
    'website': "https://www.odoo.com/",
    'category': 'Sales/Warranty Extension',
    'summary': 'Warranty Extension',
    'description': """
        Inheritance Demonstration
    """,
    'data': [
        'security/ir.model.access.csv',
        'wizard/warranty_selection_wizard.xml',
        'views/warranty_configuration_views.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
