# noinspection PyStatementEffect
{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Alessandro (alca)",
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'views/inherited_user_view.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_offer_views.xml',
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
    ]
}
