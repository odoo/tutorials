{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Odoo",
    'category': 'Category',
    'summary': """
        Real Estate Summary
    """,
    'description': """
        Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    # # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'license': 'AGPL-3',
    'application': True
}
