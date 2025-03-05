{
    'name': 'Real Estate',
    'version': '1.0',
    'sequence': 1,
    'summary': 'Help users with Real estate.',
    
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_menus.xml',

    ],
    
    'depends': [
        'base_setup'
    ],
    
    'license': 'LGPL-3'
}