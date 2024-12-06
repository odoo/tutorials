{
    'name': 'ESTATE',
    'version': '0.1',
    'category': 'Tutorials/Estate',
    'summary': 'Allow Users to Buy and Sell Property',
    'description': "",
    'website': 'https://www.odoo.com',
    'depends': [
        'base'
    ],
    'data': ['security/ir.model.access.csv',
    'views/estate_property_views.xml',
    'views/estate_property_type_views.xml',
    'views/estate_property_tags_views.xml',
    'views/estate_menus.xml'],
    'demo': [],
    'css': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
    'author':"Odoo"
}