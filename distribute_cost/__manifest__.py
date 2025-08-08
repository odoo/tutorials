# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Distribute Cost',
    'version' : '1.0',
    'description' : """
This module provides a real estate accounting services
""",
    'depends' : ['sale_management'],
    'data' : [
        'security/ir.model.access.csv',
        'views/sale_order_line_views.xml',
        'wizard/sale_order_line_wizard.xml',
    ],
    'installable' : True,
    'application' : True,
    'license' : 'LGPL-3',
}
