{
    'name': "estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Author Name",
    'category': 'Category',
    "license": "LGPL-3",
    "application": True,
    "sequence": 1,
    'data': [
     'security/ir.model.access.csv',
     'views/estate_property_views.xml',
     'views/estate_property_type_views.xml',
     'views/estate_tag_views.xml',
     'views/estate_property_offer_views.xml',
     'views/estate_menus.xml', 
     'views/inherited_model.xml',
    ],
}
