{
    'name': 'Estate',
    'category': 'Sales',
    'sequence': 1,
    'summary': 'Sell and bid on the hottest real estate properties.',
    'website': 'https://www.odoo.com/app/estate',
    'depends': [
        'base_setup',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True
}
