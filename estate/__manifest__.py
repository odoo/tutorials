{
    'name': "Estate",
    'author': "Romain ROSANO (rros)",
    'version': '0.1',
    'license': 'LGPL-3',
    'depends': ['base'],
    'category': 'Tutorials/Server',
    'application': True,
    'installable': True,
    'description': """
    This module follows the onboarding training requirements.
    This module allows to manage home selling. That's means homes can be added, modified and offers made by customers.
    """,
    'data': [
        'security/ir.model.access.csv',

        'views/salesperson_user_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_menus.xml',
        'views/estate_property_offer_views.xml'
        ],
}
