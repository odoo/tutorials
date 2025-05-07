{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Shivraj Bhapkar",
    'category': '',
    'description':'This test module',
    'application':True,
    'data': [
        'security/ir.model.access.csv',  
        'views/estate_property_views.xml', 
        'views/estate_menus.xml',
        'views/estate_property_type_views.xml', 
        'views/estate_property_offer_views.xml',
    ],

    'installable':True
}