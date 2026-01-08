{
    'name': "Supplier Portal",
    'license': 'LGPL-3',
    'depends': [
        "website",
        "account",
    ],
    'data': [
        'views/supplier_portal_controller_templates.xml',
        'views/website_supplier_portal_menu.xml',
    ],
    'installable': True,
    'auto_install': True,
}
