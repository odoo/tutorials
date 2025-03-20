{
    'name': 'Real Estate',
    'version': '1.2',
    'category': 'Tutorials',
    'sequence': 15,
    'summary': 'Tutorial base on real estate application',
    'description': "",
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/property_offer/lists.xml',
        'views/property_offer/forms.xml',
        'views/property_offer/actions.xml',

        'views/property_type/actions.xml',
        'views/property_type/forms.xml',
        'views/property_type/lists.xml',

        'views/property_tag/actions.xml',
        'views/property_tag/lists.xml',

        'views/estate_user/forms.xml',

        'views/estate_property_views.xml',
    ],
    'demo': [
    ],
    'css': ['static/src/css/crm.css'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
