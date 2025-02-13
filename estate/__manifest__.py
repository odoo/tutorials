{
    'name': "Real Estate",
    'summary': "Real Estate Module helps to buy and sell Properties.",
    'application': True,
    'category': "Tutorials",
    'installable': True,
    'depends': ['mail'],
    'data': [
        'data/estate_property_data.xml', 
        'security/ir.model.access.csv', 
        'views/estate_property_views.xml', 
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menu_views.xml',
        'views/res_user_views.xml',
    ],
    'license': 'AGPL-3',
}
