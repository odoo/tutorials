from odoo import models, fields


class InheritedUsers(models.Model):
    _inherit = "res.users"
    # error if name used - TypeError: Many2many fields inherited.users.groups_id and res.users.groups_id use the same table and columns
    # _name="inherited.users"
    property_ids = fields.One2many(
        "estate.property",
        "sales_man",
        domain=[("state", "=", "new") or ("state", "=", "offer_received")],
        string="Properties",
    )

