# -*- coding: utf-8 -*-
# licence

{
    'name': 'Real estate',
    'version': '0.0',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        
        'views/estate_property_views.xml',
        'views/ep_type_views.xml',
        'views/ep_tag_views.xml',
        'views/ep_offer_views.xml',
        # The menu seems to have to be loaded last since there are references to contents of other files instead, otherwise parse error
        'views/estate_menu_views.xml',
    ],
    'application': True
}