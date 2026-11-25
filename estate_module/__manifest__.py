{
    'name': 'estate_module',
    'version': '1.0',
    'summary': 'Sales real estates',
    'author': 'lobas',
    'license': 'LGPL-3',
    'depends': ['base', 'base_import_module'],
    'data': [
        'models/estate_property_type.xml',
        'models/estate_property_tag.xml',
        'models/estate_property.xml',
        'security/ir.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
    ],
}
