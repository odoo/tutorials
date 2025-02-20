# -*- coding: utf-8 -*-
{
    'name': "Really real Estate",
    'summary': "Some estate that really is real as f*",
    'description': "Some estate that really is real as f*",
    'installable': True,
    'application': True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
    ],
    'license': 'AGPL-3',
}
