from odoo import api, fields, models


class InheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="seller",
        string="Properties",
        domain=[('state', 'in', ['new', 'offer_received'])]
    )
