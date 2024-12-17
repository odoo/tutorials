{
    'name': 'Warranty',
    'version': '1.0',
    'category': 'Sales',
    'depends': ['base', 'sale'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'summary': 'Warranty related to products.',

    'data': [
        'security/ir.model.access.csv',
        'wizard/warranty_wizard_view.xml',
        'views/warranty_views.xml',
        'views/warranty_menu.xml',
    ]
}
