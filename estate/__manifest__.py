# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name' : "estate",
    'category' : "Real Estate/Brokerage",
    'version' : '1.0',
    'description' : """
        Real Estate Management
    """,
    'depends' : ['base','website'],
    'data' : [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_offer_wizard_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'data/estate_property_type.xml'
    ],
    'demo' : [
        'demo/demo_estate_property.xml',
        'demo/demo_estate_property_offer.xml',
    ],
    'application' : True,
    'installable' : True,
    'license': 'LGPL-3',
}
