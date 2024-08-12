{
    'name': 'estate',
    'version': '1.0',
    'summary': 'An real state management application',
    'description': 'Estate_property_module',
    'category': 'Sales',
    'author': 'YASP',
    'depends': ['base'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
}
