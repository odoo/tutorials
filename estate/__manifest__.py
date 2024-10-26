{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Harsh Chaudhari",
    'category': 'Real Estate/Brokerage',
    'description': """
    Real Estate description...
    """,
    # data files always loaded at installation
    'data': [
        'wizard/estate_property_offer_to_anyflat.xml',
        'security/security.xml',
        'data/estate.property.type.csv',
        'views/estate_property_offers_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_views.xml',
        'views/estate_menus_view.xml',
        'security/ir.model.access.csv',
        'views/res_users_inherited_view.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/estate_property_demo_date.xml',
        'demo/estate_property_offer_demo.xml'
    ],
    'application': True,
    'installable': True,
}
