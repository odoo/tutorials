from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"

    _order = "sequence, name"

    _unique_type_name = models.Constraint(
        "UNIQUE(name)",
        "The property type name must be unique.",
    )

    name = fields.Char('Name', required=True)

    sequence = fields.Integer(default=1)

    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties",
    )

    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id"
    )

    offer_count = fields.Integer(
        compute="_compute_offer_count"
    )

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
