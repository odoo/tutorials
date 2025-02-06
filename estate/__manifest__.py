{
    'name':'estate',
    'version': '1.0',
    'author': "assh-odoo",
    'depends':[
        'base'
    ],
    'data':[
        'data/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_types.xml',
        'views/estate_property_tags.xml',
        'views/estate_property_offer.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
}
