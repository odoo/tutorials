# -*- coding: utf-8 -*-
{
    'name': "Estate",
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/properties_form.xml',
        'views/estate_menus.xml',
    ],
    'license': 'LGPL-3',
}
