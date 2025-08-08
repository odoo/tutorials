{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base','website'],
    'license':'LGPL-3',
    'author': "Ajay Karma",
    'category': 'real estate/brokerage',
    'description': "Real_estate_app",
    'installable': True,
    'application': True,
    'auto-install': True,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_offer_wizard.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'views/estate_property.xml',
        "views/res_users_view.xml",
        "views/estate_website.xml",
        'views/estate_property_template.xml',
        "views/estate_property_detailed_template.xml",
        "views/estate_property_offer_template.xml",
        'views/estate_menus.xml',
    ],
    'demo':[
        'demo/estate_property_tag.xml',
        'demo/estate_property_type.xml',
        'demo/estate_property.xml',
        'demo/estate_property_offer.xml',

    ],

}

