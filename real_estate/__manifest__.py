{
    'name': 'Real estate',
    'version': '0.1.0',
    'summary': 'Manage real estate properties',
    'sequence': '1',
    'description': """
Buying & selling Properties
===========================
This Module provide functionalities from where you manage the real estate properties from finding buyer to get best price.
    """,
    'category': 'sales',
    'website': 'https://www.ishw.tech',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'Ishwar',
    'license': 'LGPL-3',
}
