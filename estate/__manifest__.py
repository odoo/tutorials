{
    'name': 'Estate',
    'depends': [
        'base_setup',
    ],
    'data':[
        'security/ir.model.access.csv',
        'views/inherited_res_users_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True
}