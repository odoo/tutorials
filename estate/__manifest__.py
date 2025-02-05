{
    'name': "estate app",
    'summary': "estate module",
    'description': "estate module for buying and selling properties. Users can buy/sell properties via estate agents",
    'author': "Odoo",
    'category': 'Tutorials/estate',
    'version': '0.1',
    'depends': ['base'],
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        ],
    'application': True,
    'installable': True,
    'license': 'AGPL-3'
}
