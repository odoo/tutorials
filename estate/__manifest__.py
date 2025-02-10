{
    'name': 'Estate',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Odoo - Rushil Patel',
    'description': 'Technical training chapter - 2',
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_menus.xml',
    ],
    'demo' : [
        'data/estate_property_demo.xml'
    ],
    'application': True
}
