# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Real Estate', # display name of the app
    'summary': 'Allows to buy and sell properties', # a short summary of app's functionality
    'description': """
    Description text
    """, # functionality of this module in detail
    'version': '1.0',
    'author': "iemu",
    'category': '',
    'depends': [ # a list of all modules this module depends on
        'base',
    ],
    'application': True, # is it an app / is it a module that will be showed in the Apps app
    'auto_install': False, # If True, this module will automatically be installed if all of its dependencies are installed
    # 'data': [ # data files always loaded at installation
        # 'views/mymodule_view.xml',
    # ],
    # 'demo': [ # data files containing optionally loaded demonstration data
        # 'demo/demo_data.xml',
    # ],
}