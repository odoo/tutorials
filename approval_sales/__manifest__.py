# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Approvals - Sales',
    'version': '1.0',
    'description': """
This Module provides Approval feature for sale quotations.
    """,
    'depends': ['sale_management', 'approvals'],
    'data': [
        'data/approval_category_data.xml',
        'views/sale_order_views.xml',
        'views/approval_category_views.xml',
        'views/approval_request_views.xml',
        'views/approval_product_line_views.xml',
    ],
    'demo': [
        'data/approval_demo.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
