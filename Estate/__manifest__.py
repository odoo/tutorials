{
    'name': "Estate",

    'description': """
        sell and manage your property
    """,

    'author': "Sourabh",
    'category': 'Tutorials/Estate',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ["base"],

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_tag_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [],

    'license': 'AGPL-3'
}
