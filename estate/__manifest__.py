{
    'name': "estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Yoann Baron (bary)",
    'category': 'Tutorials',
    'description': """
    Tutorial estate module for onboarding
    """,
    'website': 'https://www.odoo.com/page/estate',
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',

        'data/ir_sequence_data.xml',
        'demo/demo_property_types.xml',
        'demo/demo_properties.xml',
        'demo/demo_property_offers.xml',

        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/property_types_views.xml',
        'views/property_tags_views.xml',
        'views/inherited_model_views.xml',

        'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'application': True,
}