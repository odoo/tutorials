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
        'views/estate_property_type_actions.xml',
        'views/estate_property_tag_actions.xml',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
    ]
}