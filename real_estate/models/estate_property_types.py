# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstatePropertyTypes(models.Model):
    _name = "estate.property.types"
    _description = "Estate Property Types"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    offer_ids = fields.One2many(comodel_name="estate.property.offers", inverse_name="property_type_id")
    offer_count = fields.Integer(string="Number of Offers", compute="_compute_offer_count")
    property_ids = fields.One2many("estate.property", "estate_property_type_id", string="Properties")

    _sql_constraints = [
        (
            "unique_type_name",
            "UNIQUE(name)",
            "This property type already exits, create a unique one.",
        )
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
