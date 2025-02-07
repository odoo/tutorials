{
    'name': "Real Estate",
    'description': """ The Real Estate Advertisement module. """,
    'license': 'LGPL-3',
    'application': True,
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
    ],
    
}
