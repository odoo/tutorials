{
    'name': 'Estate',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_config_parameter_data.xml',
        'data/estate_types.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_res_user_views.xml',
        'views/res_config_settings_views.xml',
        'views/estate_menu_views.xml'
    ],
    'demo': [
        'demo/demo_property_data.xml',
        'demo/demo_offer_data.xml'
    ],
    'application': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3'
}
