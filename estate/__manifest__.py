# -*- coding: utf-8 -*-
{
    'name':"estate",
    'description':"test",
    'depends': [
        'base_setup'
    ],
    'category': "Tutorials",
    'installable': True,
    'application': True,
    'data':[
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menu_views.xml',
        'security/ir.model.access.csv']

}