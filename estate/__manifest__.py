{
    'name': 'Real Estate',
    'version': '1.0',
    'description': 'Real Estate Management System',
    'summary': 'Real Estate Management System',
    'author': 'Lud0do1202',
    'license': 'LGPL-3',
    'depends': [
        'base'
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Views
        'views/estate_property.xml',
        'views/estate_menus.xml',
    ],
    'auto_install': False,
    'application': True,
}