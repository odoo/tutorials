from odoo import models, fields


class Estate_inherited_model(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate_property", "salesperson_id", string="Properties")
