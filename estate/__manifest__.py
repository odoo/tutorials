{
    'name': 'Estate',
    'description': """
        It is an application made for users for a purchase and sales
        of there properties and make experience smoother
        """,
    'sequence': 1,
    'depends' : ['base'],
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'models/menus/estate_menus.xml'
        ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}