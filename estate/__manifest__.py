{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Hitesh Prajapati",
    'category': 'tutorials/estate',
    'license': 'LGPL-3',
    'description': """
    Description text
    """,
    'application': True,
    'instalable': True,

    'data':[
        'data/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml'
    ],
    'demo':[
        
    ]
    
}