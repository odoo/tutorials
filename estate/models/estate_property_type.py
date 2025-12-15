from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)

    # Relations
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")

    # Computed
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self) -> None:
        for record in self:
            record.offer_count = len(record.offer_ids)

    # Constraints
    _uniq_name = models.Constraint(
        "UNIQUE(name)",
        "A property type's name must be unique.",
    )
