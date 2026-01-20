{
    'name': 'Supplier Portal',
    'version': '1.0',
    'depends': ['website', 'accountant'],
    'description': """
This module allows suppliers to log in and generate vendor bill by uploading PDF/XML invoice files.
""",
    'data': [
        'data/supplier_portal_website_menu.xml',
        'views/supplier_portal_view.xml'
    ],
    'license' : 'LGPL-3'
}
