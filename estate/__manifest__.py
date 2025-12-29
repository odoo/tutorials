{
    'name': "estate",
    'description': "test",
    'depends': [
        'base_setup'
    ],
    'category': "Tutorials",
    'installable': True,
    'application': True,
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menu_views.xml',
        'views/res_user_views.xml',
        'security/security.xml',
        'security/ir.model.access.csv'],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3'

}
