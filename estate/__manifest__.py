{
    'name': 'Real Estate',
    'version': '0.0',
    'category': 'Sale/estate',
    'summary': 'Manage your Real Estate Assets',
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ]
}
