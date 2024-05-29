{
    'name': "estate",
    'depends': ['base'],
    'author': "sndibwami@virunga.org",
    'license': "AGPL-3",
    'summary': "Real Estate Management",
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'demo': [
        'demo/demo.xml',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
}