# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Real Estate",
    'category': "Real Estate/Brokerage",
    'version': "1.0",
    'author': "rsbh",
    'description': "A module for managing real estate properties",
    'depends':['base', 'website'],
    'data': [
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_offer_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_view.xml',
        'views/res_users_view.xml',
        'views/estate_menus.xml',
        'wizard/estate_property_wizard_view.xml',
        'views/estate_property_web_temp.xml',
        'views/website_menu.xml',
        'data/estate_data.xml'
    ],
    'demo': [
         'demo/estate_property_demo.xml',
         'demo/estate_property_offer_demo.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': "LGPL-3",
}
