# -*- coding: utf-8 -*-
{
    'name': "Estate",

    'depends': [
        'base'
    ],

    'data' : [
        'security/ir.model.access.csv',

        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml'
    ],
    'application': True


}
