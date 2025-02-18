import odoo

if odoo.tools.config.get("test_enable"):
    from . import test_estate 