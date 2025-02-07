{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base'],
    'author': 'ATPA',
    'category': 'Category',
    'description': """
Real Estate module is for training
""",
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml'
    ],
    'application' : True
}
