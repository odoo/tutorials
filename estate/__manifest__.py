{
    'name': 'Estate',
    'category': 'Tutorials',
    'depends': ['base', 'mail'],
    'application': True,
    'installable': True,
    'author': 'vikvi',
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/mail_template.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_user_views.xml',
        'views/estate_validity.xml'

    ],
}
