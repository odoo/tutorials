{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate Sales Management',
    'author': 'UMBM',
    'summary': 'Manage appartments rent',
    'description': "",
    'license': "GPL-3",
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
    ],
    'installable': True,
    'application': True,
}
