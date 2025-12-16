{
    'name': "Estate",

    'summary': """
        Starting module for "Estate"
    """,

    'description': """
        Starting module for "Estate"
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tutorials',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],
    'data': [
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'installable': True,
    'license': 'AGPL-3'
}
