{
    'name': 'estate',
    'author': 'Odoo S.A.',
    'depends': ['base'],
    'application': True,
    'license': 'LGPL-3',

    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',

        'views/estate_menus.xml',

        'views/res_users_view_form.xml',

    ],
}
