{
    'name': 'Real Estate',
    'version': '1.0',
    'license': 'LGPL-3',
    'summary': 'Real estate advertisement management',
    'description': """
        Real Estate tutorial module.
    """,
    'author': 'Parth Sawant',
    'depends': ['base'],
    'category': 'Real Estate',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/demo.xml',
        'demo/demo_tag.xml',
        'demo/demo_type.xml',
    ],
    'application': True,
}
