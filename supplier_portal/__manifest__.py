{
    'name': "Supplier Portal",
    'description': "Generates vendor bill when supplier upload pdf/xml file",
    'author': "Samit Bhadiyadra - sbbh",
    'depends': [
        "website",
        "account",
    ],
    'data': [
        'views/supplier_portal_template.xml',
        'views/supplier_portal_menu.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
