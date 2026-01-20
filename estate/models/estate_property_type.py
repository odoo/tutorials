from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of Real Estate Properties"
    _order = "sequence,name"

    name = fields.Char(required=True, string="Property Type")
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    sequence = fields.Integer("Sequence")
    offer_ids = fields.One2many(
    "estate.property.offer", "property_type_id", string="Offers"
)
    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer_count")

    _sql_constraints = [
        ("unique_type_name", "UNIQUE(name)", "Property type name must be unique."),
    ]

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
