from odoo import fields, models

class ResUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "user_id", string="Property Id",
                    domain=[('state', 'in', ['new', 'offer_received'])]
)
