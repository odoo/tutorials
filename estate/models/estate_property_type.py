
from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The type of a property"
    _order = "name"

    _sql_constraints = [
        (
            "name",
            "unique(name)",
            "The name of the property type must be unique.",
        )
    ]

    name = fields.Char(required=True)
    properties_ids = fields.One2many("estate.property", string="Properties", inverse_name="property_type_id")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")
    sequence = fields.Integer("Sequence", default=1)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
        
