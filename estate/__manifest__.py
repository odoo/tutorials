{
    'name': 'Real Estate',
    'category': 'All',
    'summary': 'Demo app for estate',
    'description': "This is the demo app ",
    'installable': True,
    'depends': ['base'],
    'application': True,
    'auto_install': False,
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ]
}