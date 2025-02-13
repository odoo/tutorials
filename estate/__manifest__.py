{
    'name': "estate",
    'depends': ['base','mail'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tags_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml'

    ],
    'license': 'LGPL-3'  
}
