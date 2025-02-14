{
    'name': 'Estate Module',
    'version': '1.0',
    'category': 'Real Estate/Brokerage',
    'depends': ['base'],
    'sequence' : 1 ,
    'description' :""" This is the real estate module """,
    'license':'LGPL-3' ,
    'installable':'True' ,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags.xml',
        'views/estate_menus.xml',       
        'views/res_user_view.xml',
        'data/master_data.xml'
    ],
    "demo": [
        "demo/demo_data.xml",
    ]
    "application": True,
}
