{
    'name': "estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Author Name",
    'category': 'Category',
    'summary': 'Manage estate offers',
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_actions.xml',
        'views/estate_property_menus.xml',
        'views/estate_property_views.xml',
    ]
}