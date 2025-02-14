# Part of Odoo. See LICENSE file for full copyright and licensing details.
import odoo 

if odoo.tools.config.get("test_enable"):
    from . import test_estate
