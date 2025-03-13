{
    'name': 'Multiple Approval Mechanism',
    'version': '1.0',
    'description': 'Multiple Approval Mechanism',
    'author': 'Manthan Akbari ',
    'license': 'LGPL-3',
    'summary': "A Multiple Approval Mechanism Module",
    'depends': [
        'sale_management', 'approvals'
    ],
    'auto_install': True,
    'data': {
        'data/approval_demo_data.xml',
        'views/approval_category_views.xml',
        'views/sale_order_views.xml',
        'views/approval_request_views.xml',
    }
}
