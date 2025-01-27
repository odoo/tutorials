{
    'name': 'Sell Product Kit',
    'description': "Module to add function to sell product as a kit.",
    'installable': True,
    'application': False,
    'depends': ['product', 'sale', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_form_view_inherited.xml',
        'wizard/product_kit_view_wizard.xml',
        'views/view_order_form_inherited.xml',
        'report/sale_order_document_report.xml',
        'report/sale_portal_templates_report.xml'
    ],
    'license':'LGPL-3'
}
