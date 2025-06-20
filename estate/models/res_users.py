from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    properties_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="user_id",
        domain=[("state", "in", ['new', 'offer_received'])],
        string="Properties"
    )
