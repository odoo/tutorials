from odoo import api, fields, models


class EstateType(models.Model):
    _name = "estate.type"
    _description = "An estate type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(required=True, default=1)

    # Foreign fields
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.offer", "property_type_id")

    # Computed fields
    offer_count = fields.Integer(compute="_compute_offer_count")

    # Constraints
    _check_name = models.Constraint(
        "UNIQUE(name)",
        "A type must be unique",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
