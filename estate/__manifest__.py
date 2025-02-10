{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Property',
    'depends': ['base'],
    'sequence': 15,
    'summary': 'Find various properties in a click',
    'description': "",
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
        'views/res_users_view.xml',
        'security/ir.model.access.csv'
    ]
}
