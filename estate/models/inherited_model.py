from odoo import fields, models


class Estate_users_model(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson_id", string=" Estate properties")
