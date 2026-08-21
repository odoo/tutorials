{
    'name': "A Real Estade Advestisement Demo",
    'version': '1.0',
    'depends': ['base'],
    'author': "Odoo S.A.",
    'category': 'Sales',
    'description': """
    Test module for managing real estade advertisement
    created as part of the onboarding.
    """,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',

        'views/estate_menus.xml',
    ],
}
