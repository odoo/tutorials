{
   'name': "Estate",
   'version':"1.0",
   'depends': ['base','account'],
   'author':"bhpr",
   'category': 'RealEstate/Brokerage',
   'description': """
        Starting module of Real Estate 
    """,
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_offer.xml',
        'views/estate_menus.xml'
    ],
    'license':'LGPL-3',
    'installable': True,
    'auto_install': True,
    'application': True,  
}
