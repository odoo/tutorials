{
    'name': 'real_estate',
    'version': '0.1',
    'category': 'sales',
    'summary': 'Manage real estate properties',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'Ishwar',
    'license': 'LGPL-3',
}
