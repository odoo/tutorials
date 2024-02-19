{
    'name': 'ESTATE',
    'version': '1.0',
    'category': 'buildings',
    'website': 'https://www.odoo.com/page/estate',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True
}
