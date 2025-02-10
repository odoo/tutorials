{
    'name': "estate",
    'version': '1.0',
    'summary': "Manage real estate properties, offers, and sales",
    'sequence': 15,
    'description': """ 
        This module helps manage real estate properties, track offers, and handle sales.
    """,
    'category': 'Real Estate',
    'author': "Darshan Patel",
    'website': "",
    'depends': ['base'],
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_tag.xml',
        'views/res_user.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}