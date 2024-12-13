{
   'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base'],
    'author': 'insh',
    'category': 'Estate',
    'license' : 'LGPL-3',

    'data' : [
        'security/ir.model.access.csv',
        
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}