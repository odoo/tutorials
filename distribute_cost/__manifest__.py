{
    'name': 'Distribute Cost',
    'version': '1.0',
    'summary': 'Distribute Cost Over other sales line',
    'author': 'chirag Gami(chga)',
    'category': 'Sales',
    'depends': ['base', 'sale_management', 'account'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/price_division_wizard_view.xml',
        'views/sale_order_pdf_template.xml',
        'views/sale_order_portal_template.xml',
    ],
    'installable': True,
    'application': True,
}
