from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence,name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
    )
    sequence = fields.Integer(default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _unique_name = models.Constraint(
        "unique(name)",
        "The property type name must be unique.",
    )

    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
