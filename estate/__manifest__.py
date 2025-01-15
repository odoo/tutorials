{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base', 'website'],
    'author': "Kishan B. Gajera",
    'category': 'Real Estate/Brokerage',
    'description': """
        Estate App
    """,


    'application': True,
    'installable': True,

    'license':'LGPL-3',

    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offers_view.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'data/estate.property.type.csv',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'wizard/estate_property_make_offer_wizard.xml',
        'views/estate_proeprty_web_view.xml'
    ],
    'demo': [
        'demo/estate_property_demo.xml',
        'demo/estate_property_offers_demo.xml',
    ],
}