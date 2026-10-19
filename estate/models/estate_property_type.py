from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name"

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The property type name must be unique.",
    )

    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence", default=10)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offers Count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
