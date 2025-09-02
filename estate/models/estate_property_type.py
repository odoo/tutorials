
from odoo import api, fields, models


# estate.property.type model
class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type database table"
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties")
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer(string="Sequence")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_ids")
    _sql_constraints = [
        (
            "unique_property_type",
            "unique(name)",
            "Property type should be unique",
        ),
    ]

    @api.depends("offer_ids")
    def _compute_offer_ids(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
