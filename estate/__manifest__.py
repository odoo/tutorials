{
    'name':'estate',
    'author':'dijo',
    'version':'1.2',
    'summary':'This is real-estate module developed by deep i. joshi',
    'application': True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv', 
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_user_view.xml',
        'views/estate_property_views.xml',
        'views/estate_property_menu.xml',
    ]
}