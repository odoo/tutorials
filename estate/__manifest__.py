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
        'views/estate_property_views.xml', #Load Property model views
        'views/estate_property_type_views.xml', #Load Property Type model views
        'views/estate_property_tag_views.xml', #Load Property Tag model views
        'views/estate_menus.xml', #Load menus after views
    ],
    'license':'LGPL-3'
}