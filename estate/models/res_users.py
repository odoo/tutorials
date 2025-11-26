from odoo import fields, models


class ResUsers(models.Model):
    # ----------------------------------------
    # Private attributes
    # ----------------------------------------
    _inherit = "res.users"

    # ----------------------------------------
    # Field declarations
    # ----------------------------------------
    property_ids = fields.One2many("estate.property", "salesperson_id", string="Real Estate Properties")
