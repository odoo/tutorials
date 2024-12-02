# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Estate',
    'category': 'Tutorials/Estate',
    'summary': 'Real estate application',
    'description': "",
    'depends': [
        'base_setup',
    ],
    'data': [
      'security/ir.model.access.csv',
      'views/estate_property_views.xml',
      'views/estate_property_tag_views.xml',
      'views/estate_property_type_views.xml',
      'views/estate_property_offer_views.xml',
      'views/res_users_views.xml',
      'views/estate_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OEEL-1'
}
