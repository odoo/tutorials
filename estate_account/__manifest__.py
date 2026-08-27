{
    'name': "Estate Account",

    'summary': """
        Tutorial module for estate account management
    """,

    'description': """
        Tutorial module for estate account management
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tutorials',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'estate', 'account'],
    'application': False,
    'installable': True,
    'data': [
    ],
    'assets': {
    },
    'license': 'AGPL-3'
}
