{
    'name': 'Estate',
    'description': 'Estate Module',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Shiv Bhadaniya',
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_res_users_views.xml',
        'views/estate_menus.xml',
    ]
}
