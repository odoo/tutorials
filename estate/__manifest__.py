{
    'name': 'Real Estate',
    'summary': 'Manage real estate properties',
    'description': "",
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_list.xml',
        'views/estate_property_form.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'category': 'Real Estate/Estate',
    'menu_icon': 'fa-home',
}
