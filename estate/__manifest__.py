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
        # 'security/security.xml',  # Reference to the security.xml file
        # Add other XML files here like views, data, etc.
        'views/estate_property_views.xml',  # Action for estate.property
        'views/estate_menus.xml',
        # Other XML files (views, templates, etc.)
    ],
    'category': 'Test',
    'installable': True,
    'application': True,
    # 'auto_install': False,
    'license': 'LGPL-3',
     
}