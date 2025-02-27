{
    'name': "Product Kit",
    'version': '1.0',
    'category': 'Sales/Sales',
    'description': "Add new feature to sell product as kit",
    'depends': [
        'sale_management'  # -> sale, digest
    ],
    'data': [
        'security/ir.model.access.csv',

        'report/ir_actions_report_templates.xml',

        'wizard/subproduct_wizard_view.xml',

        'views/product_views.xml',
        'views/sale_order_views.xml',
        'views/sale_portal_templates.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
