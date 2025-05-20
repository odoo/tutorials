{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'sequence': 15,
    'summary': 'Track Real Estate',
    'description': "This app is made for real estate tracking.",
    'website': 'https://www.odoo.com/page/estate',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
