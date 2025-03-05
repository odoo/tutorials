# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Distribute sale line",
    'version': '1.0',
    'category': "Sales/Sales",
    'description': """
        Distribute cost over other sale lines.
    """,
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        'views/sale_order_line_views.xml',
        'views/sale_order_line_distribution_wizard_views.xml',
        'views/source_sale_order_line_wizard.xml',
    ],
    'installable': True,
    'license': "LGPL-3",
}
