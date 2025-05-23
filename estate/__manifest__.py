{
    'name': "Real Estate",
    'version': '0.1',
    'category': 'Tutorials/Estate',
    'summary': "Real estating module",

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_types.xml',
        'views/estate_property_tags.xml',
        'views/estate_property_offers.xml',
        'views/res_users.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'depends': ['base'],
    'license': 'AGPL-3'
}
