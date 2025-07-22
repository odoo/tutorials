{
    'name': "Real Estate",
    'version': '18.0',
    'depends': ['base'],
    'author': "Rahul Jha (jhra)",
    'website': "https://www.odoo.com",
    'category': 'Real Estate/Brokerage',
    'description': """
    Test module for selling real estate properties.
    """,
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'report/estate_property_reports.xml',
        'report/estate_property_template.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
    ],
    'demo': [
        'demo/estate.property.type.csv',
        'demo/estate_property_demo.xml',
        'demo/property_with_offers.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3'
}
