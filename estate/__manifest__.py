{
    'name': "estate app",
    'summary': "estate module",
    'description': "Estate module for buying and selling properties. Users can buy/sell properties via estate agents",
    'author': "Odoo",
    'category': 'Tutorials/estate',
    'version': '1.0',
    'depends': ['base'],
    'data':[
        'security/ir.model.access.csv',
        #'security/security.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'AGPL-3'
}

