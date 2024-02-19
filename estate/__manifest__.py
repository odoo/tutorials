{
    'name': 'Estate',
    'version': '1.2',
    'category': 'Estate',
    'summary': 'Estate application',
    'description': "",
    'website': 'https://www.odoo.com/page/estate',
    'depends' : [
        'base',
    ],
    'data': [
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
    'application': True,
}
