{
    'name': 'estate',
    'version': '1.0',
    'summary': "It is a very useful app",
    'description': "This is a demo estate module",
    'category': 'Tools',
    'author': 'Abhishek Patel',
    'license': 'LGPL-3',
    'depends': ['base'],
    'installable': True,
    'application': True,

    # This data field loads all required files to run the module
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_offer_views.xml'
    ],
}
