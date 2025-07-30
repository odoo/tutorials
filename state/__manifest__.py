{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Roxana",
    'category': 'Category',
    'description': """
    Módulo de Publicidad Inmobiliaria
    """,
    'data': [
       'security/ir.model.access.csv',
       'views/res_users_views.xml',
       'views/estate_property_offer_views.xml',
       'views/estate_property_tags_views.xml',
       'views/estate_property_type_views.xml',
       'views/estate_property_views.xml',
       'views/estate_menu.xml'
    ],
    'application': True,
    'license': 'LGPL-3',
}