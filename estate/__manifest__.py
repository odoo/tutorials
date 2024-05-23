{
    'name': 'estate',
    'depends': ['base'],
    'installable': True,
    'application': True,
    'version': '1.0',
    'category': 'Sales',
    'description': 'Module for estate property',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus_views.xml',
        'views/estate_list_views.xml',
        'views/estate_search_views.xml',
    ],
    'license': 'LGPL-3',
}
