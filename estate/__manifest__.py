{
    'name': 'Estate',
    'description': """
        A module to manage real estate properties including their details, status, and sales.
    """,
    'depends': ['base'],
    'application': True,
    'author': 'Soukaina Tyes',
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_list_view.xml',
        'views/estate_property_form_view.xml',
        'views/estate_property_search_view.xml',
    ]
}
