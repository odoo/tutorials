{
   'name': "Estate",
   'version':"1.0",
   'depends': ['base','account'],
   'author':"bhpr",
   'category': 'RealEstate/Brokerage',
   'description': """
        Starting module of Real Estate
    """,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_res_users.xml',
        'views/estate_property.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_offer.xml',
        'views/estate_menus.xml',
        'data/estate_property_type.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'wizard/estate_offer_wizard.xml',
        'views/estate_property_template.xml'
    ],
    'demo': [
        'demo/estate_demo_data.xml',
    ],
    'license':'LGPL-3',
    'installable': True,
    'auto_install': True,
    'application': True,
}
