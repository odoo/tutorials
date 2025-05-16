{
    'name': 'Payment Term Discount',
    'license': 'LGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_payment_term_discount_views.xml',
        'views/account_payment_term_views.xml',
        'wizard/account_payment_register_views.xml',
    ],
    'auto_install': True,
    'post_init_hook': '_payment_term_discount_post_init',
}
