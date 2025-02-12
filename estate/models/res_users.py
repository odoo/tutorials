from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"
    # error if name used - TypeError: Many2many fields inherited.users.groups_id and res.users.groups_id use the same table and columns
    # _name="inherited.users"
    property_ids = fields.One2many(
        "estate.property",
        "user_id",
        domain=[("state", "=", "new") or ("state", "=", "offer_received")],
        string="Properties",
    )

