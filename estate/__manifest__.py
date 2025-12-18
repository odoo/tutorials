{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Sales',
    'sequence': 1,
    'summary': 'Sell and bid on the hottest real estate properties.',
    'website': 'https://www.odoo.com/app/estate',
    'depends': [
        'base_setup',
        'mail',
        'calendar',
        'contacts',
        'phone_validation',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True
}