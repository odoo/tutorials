{
    'name': "Estate",
    'version': '1.0',
    'summary': 'Training sandbox',
    'depends': [
        'base'
    ],
    'author': "XAFR",
    'license': 'LGPL-3',
    'description': """
    An application module that aims to serve as an onboarding sandbox.
    """,
    'application': "True",
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'data/estate_menus.xml',
    ],
}
