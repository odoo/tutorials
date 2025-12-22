{
    'name': "Estate",

    'author': "Odoo",
    'website': "https://www.odoo.com",

    'category': 'Tutorials',
    'version': '1.0',

    'depends': ['base', 'web'],
    'data': [
        'views/estate_property_offer_view.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_search_view.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'installable': True,
    'license': 'AGPL-3'
}
