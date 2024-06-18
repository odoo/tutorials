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
        'data/estate_property_offer_views.xml',
        'data/estate_property_views.xml',
        'data/property_types_views.xml',
        'data/property_tags_views.xml',
        'data/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'application': True,
}