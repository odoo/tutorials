from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    # Domain doesn't work
    property_ids = fields.One2many("estate.property", "seller_id", string="Properties List",
    domain=[('available_from', '<=', 'today'), ('stage', '!=', 'cancelled'), ('stage', '!=', 'sold')])
