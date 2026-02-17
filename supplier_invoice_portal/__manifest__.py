{
    'name': "Supplier Portal",
    'version': '1.0',
    'author': "Dhrudeep",
    'category': "Supplier Portal",
    'summary': "The task is that the supplier will login with portal user and will upload PDF + XML from portal to create a draft vendor bill",
    'depends': ['website', 'account'],
    'data': [
        'views/portal_home_inherit.xml',
        'views/supplier_upload_templates.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
