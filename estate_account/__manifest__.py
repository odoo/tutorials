# -*- coding: utf-8 -*-
{
    'name': 'Estate Account',
    'version': '1.2',
    'category': 'Tutorials',
    'sequence': 15,
    'summary': 'Tutorial base on real estate accounting',
    'description': "",
    'depends': [
        'base', 'estate', 'account'
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property/actions.xml',
        'views/estate_property/menus.xml',
        'views/estate_property/lists.xml',
        'views/estate_property/forms.xml',
        'views/estate_property/searchs.xml',
    ],
    'demo': [
    ],
    'css': ['static/src/css/crm.css'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
