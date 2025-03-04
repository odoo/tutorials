# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Website Appointment Filter",
    "summary": "Adds filters to website appointment booking",
    "version": "1.0",
    "author": "Nisarg",
    "category": "Website Appointment",
    "depends": [
        "website_appointment",
        "appointment_account_payment",
    ],
    "data": [
        "views/website_appointment_filter.xml",
    ],
    "auto-install" : True,
    "application": False,
    "license": "LGPL-3"
}
