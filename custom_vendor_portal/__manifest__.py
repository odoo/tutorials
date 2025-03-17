{
    'name': 'Custom Vendor Portal',
    'version': '1.0',
    'summary': 'Vendor Portal with Purchase Order Creation',
    'author': 'Nisarg Mistry',
    'category': 'Website',
    'depends': ['website', 'purchase'],
    'data': [
        'security/product_acl.xml',
        'views/vendor_portal_template.xml'
    ],
    'installable': True,
    'license': 'LGPL-3'
}
