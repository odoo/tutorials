# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Real estate',
    'version': '0.0',
    'category': 'Estate',
    'summary': 'Manage real estate',
    'description': "",
    'website': 'https://www.odoo.com/page/crm',
    'depends': [
        'base',
    ],
'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
