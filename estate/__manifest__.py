{
    'name': "Estate",
    'summary': """
        The Real Estate Advertisement module
    """,

    'description': """
        The Real Estate Advertisement module
    """,
    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'version': '19.0.0.1.0',
    'application': True,
    'depends': [
        'base',
    ],
    'data': [
        'data/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    'license': 'LGPL-3',
}
