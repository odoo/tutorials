{
    'name': 'Real Estate',
    'category': 'Tutorials/Estate',
    'summary': 'Track real estate assets',
    'description': "",
    'depends': ['base'],
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_users_form.xml'
    ],
    'license': 'AGPL-3'
}
