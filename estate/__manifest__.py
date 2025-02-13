{
    'name': "Real Estate",
    'version': '18.0',
    'depends': ['base'],
    'author': "Rahul Jha (jhra)",
    'website': "https://www.odoo.com",
    'category': 'Tutorials/RealEstate',
    'description': """
    Test module for selling real estate properties.
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3'
}
