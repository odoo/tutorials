{
    'name': 'Estate',
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
        # 'views/estate_type_menu.xml'
    ],

    'installable': True,
    'application': True
}
