# -*- coding: utf-8 -*-
{
'name': "Real Estate in Odoo",
'version':"1.0.0",
'depends': ['base'],
'application': True,
'description': 'Property management functions',
'author': 'brpac',
'data': ["security/ir.model.access.csv", 
"views/estate_property_views.xml",
"views/estate_property_type_views.xml",
"views/estate_property_tag_views.xml",
"views/estate_property_offer_views.xml",
"views/estate_menus.xml",
],
}