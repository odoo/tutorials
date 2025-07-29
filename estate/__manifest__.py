{
    'name': 'Estate',
    'depends': [
        'base_setup', 'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/ninja_turtles_estate_views.xml',
        'views/ninja_turtles_estate_property_offer_views.xml',
        'views/ninja_turtles_estate_property_type_views.xml',
        'views/ninja_turtles_estate_property_tag_views.xml',
        'views/ninja_turtles_estate_property_kanban.xml',
        'views/ninja_turtles_estate_menus.xml',
        'views/res_users_views.xml',
    ],
    'license': 'LGPL-3',
    'application': True
}
