{
    'name': 'Installment Management',
    'version': '1.0',
    'category': 'Sales',
    'author': 'odoo',
    'depends': ['base', 'sale_subscription'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/action_open_emi_wizard_view.xml',
        'data/installments_product_data.xml',
        'view/res_config_setting_view.xml',
        'view/installments_view.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
