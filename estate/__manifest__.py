{
    'name': "Real State",
    'version': '1.0',
    'depends': ['base'],
    'author': "kiro",
    'category': 'Category',
    'description': """
    Description text
    """,
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml', 
        'views/estate_menus.xml'
    ]
}
