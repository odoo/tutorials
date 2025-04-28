# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class PropertyType(models.Model):
    _name = "property.type"
    _description = "Property Types"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    property_offer_ids = fields.One2many("property.offer", "property_type_id")
    sequence = fields.Integer("Sequence", default=1, help="Used to types.")
    _order = "sequence, name"
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
        (
            "unique_type_name",
            "UNIQUE(name)",
            "Property type must be unique.",
        ),
    ]

    @api.depends("property_offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.property_offer_ids)
