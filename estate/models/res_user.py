from odoo import fields, models 


class ResUser(models.Model):
    _inherit = "res.user"

    property_ids = fields.One2many(
        "estate.property", "salesperson_id",
        domain="[('state', 'in', ['new', offer'])]"
    )
