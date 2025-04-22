{
    'name': "Real Estate",
    'depends': [
        'base_setup',
    ],
    
    'application': True,
     'data': [
        'security/ir.model.access.csv',
        'views/re_action_model.xml',
        'views/estate_menus.xml',
     ]
}