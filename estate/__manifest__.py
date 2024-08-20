{
    'name': 'Estate',
    'version': '1.0',
    'depends': [
        'base'
    ],
    'author': 'romo',
    'description': """
    Housing Estate Application: create and manage housing estate offers with customized tags and housing types, and automatically generate invoicing upon sale.
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
        'views/estate_menu.xml'
    ],
    'application': True,
    'license': 'LGPL-3'
}
