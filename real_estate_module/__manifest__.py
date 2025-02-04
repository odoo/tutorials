# -*- coding: utf-8 -*-
{
    'name': "Real Estate Module",
    'summary': "Manage real estate properties.",
    'description': "This is the real estate module used for buying and selling properties!",
    'version': '0.1',
    'application': True,
    'category': 'Tutorials',
    'installable': True,
    'depends': ['base'],
    'data': [
    'security/ir.model.access.csv',
    'views/estate_property_views.xml',
    'views/estate_menus.xml',
    'data/estate_property_data.xml'

],


    'license': 'AGPL-3'
}