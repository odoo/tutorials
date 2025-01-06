{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Kishan B. Gajera",
    'category': 'real-estate',
    'description': """
        Estate App
    """,


    'application': True,
    'installable': True,

    'license':'LGPL-3',

    'data': [
        'data/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offers_view.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_menus.xml'
    ],
    'demo': [],
}