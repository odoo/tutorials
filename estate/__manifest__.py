{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'tutorials',
    'depends': ['base'],
    'summary': 'Chapter 2: Server Framework 101',
    'description': "",
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',  #Load security first
        'views/estate_property_views.xml', #Load model views
        'views/estate_menus.xml', #Load menus after views
    ],
}