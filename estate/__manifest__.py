{
    'name': 'Real estate module',
    'version': '1.0',
    'depends': ['base', 'contacts'],
    'author': 'Anton Romanova <contact@antonromanova.com>',
    'category': 'Sales',
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_actions.xml',
        'views/estate_search.xml',
        'views/estate_form.xml',
        'views/estate_list.xml',
        'views/estate_menus.xml',
        'views/res_partner_form.xml',
    ],
}
