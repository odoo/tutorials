{
    'name': 'Estate Module',
    'version': '1.0',
    'category': 'Property',
    'depends': ['base'],
    'sequence' : 1 ,
    'description' :""" This is the real estate module """,
    'license':'LGPL-3' ,
    'installable':'True' ,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
        'views/res_user_view.xml'
    ]
}


