{
    'name': "Real Estate",
    'depends': ['base'],
    'author': "Odoo",
    'category': 'Category',
    'license': 'LGPL-3',
    'application': True,
    'description': """
    A app for real estate
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_views.xml',
        'views/estate_list_views.xml',
        'views/estate_form_views.xml',
        'views/estate_search_views.xml',
        'views/estate_menus.xml',
        'views/estate_kanban_views.xml',
    ],
}
