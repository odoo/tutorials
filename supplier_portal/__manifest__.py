{
    'name': 'Supplier Portal',
    'version': '1.0',
    'description': 'Vendor bill generation portal for suppliers',
    'depends': ['account', 'website'],
    'data': [
        'views/supplier_portal_template.xml',
        'views/website_menu.xml'
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
