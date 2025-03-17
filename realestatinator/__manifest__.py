# -*- coding: utf-8 -*-

{
	'name': 'real-estate-inator',
	'description': 'Inator that helps you find real estate.',
	'category': 'Tutorials/RealEstateInator',
	'author': 'Prout!',
	'depends': [
		'base',
		'web',
	],
	'data': [
		'security/ir.model.access.csv',
		'views/estate_property_views.xml',
		'views/estate_menus.xml',
	],
	'installable': True,
	'application': True,
	'auto_install': False,
	'version': '0.1',

}
