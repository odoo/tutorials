{
    'name': "Estate",
    'version': '1.01',
    'depends': ['base'],
    'author': "berm-odoo",
    'category': 'Tutorials',
    'description': "Estate management",
    'license': "LGPL-3",
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_views.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True
}
