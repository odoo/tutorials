{
    'name': 'Real Estate',
    'license': 'LGPL-3',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Odoo S.A.',
    'category': 'Category',
    'description': """
    Real Estate Advertisement module
    """,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_list_views.xml',
        'views/estate_property_form_views.xml',
        'views/estate_property_search_views.xml',
        'views/estate_property_offer_list_views.xml',
        'views/estate_property_offer_form_views.xml',
        'views/estate_property_type_form_views.xml',
        'views/estate_property_type_list_views.xml',
    ],
}
