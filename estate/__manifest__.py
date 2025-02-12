{
    'name':'estate',
    'author':'dijo',
    'version':'1.2',
    'summary':'This is real-estate module developed by deep i. joshi',
    'application': True,
    'depends': ['base'],
    'category':'Real Estate/Brokerage',
    'data': [
        'security/ir.model.access.csv', 
        'security/security.xml',
        'data/property_type_data.xml',
        'demo/property_demo_date.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_user_view.xml',
        'views/estate_property_views.xml',
        'views/estate_property_menu.xml',
    ]
}