from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="user_id",
        string="Properties",
        domain=[("status", "not in", ["sold", "cancelled"])],
    )
