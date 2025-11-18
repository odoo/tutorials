# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


manifest = {
    "name": "Estate",
    "version": "1.0",
    "depends": ["base"],
    "data": [
        "data/ir.model.access.csv",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
