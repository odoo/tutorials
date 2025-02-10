{
    'name': 'Real estate',
    'version': '1.0',
    'author' : "sujal asodariya",
    "description": "Real estate module for managing property listings and transactions!",
    'depends': [
        'base'
    ],
    'data':[
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tags.xml',
        'views/estate_property_views.xml',  
        'views/estate_menus.xml',
      
    ],
    'category': 'Test',
    'installable': True,
    'application': True,
    # 'auto_install': False,
    'license': 'LGPL-3',
     
}