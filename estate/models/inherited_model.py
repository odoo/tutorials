from odoo import fields, models


class InheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "seller_id", string="Properties (Salesperson)", domain="[('seller_id.state', 'in', ['new', 'cancelled'])]")
