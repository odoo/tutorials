{
    'name': 'Real Estate',

    'description': """
    Real Estate Application.
    """,

    'summary': """
    Real Estate Application for beginner.
    """,

    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_menus_views.xml',
    ],

    'author': 'Mayankkumar Patel (pmad)',

    'category': 'Tutorials/RealEstate',
    'version': '1.0',

    'application': True,
    'installable': True,
}
