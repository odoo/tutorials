# licence

{
    'name': 'Real estate',
    'version': '0.0',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/ep_type_views.xml',
        'views/ep_tag_views.xml',
        'views/ep_offer_views.xml',

        'views/estate_menu_views.xml',
    ],
    'application': True
}
