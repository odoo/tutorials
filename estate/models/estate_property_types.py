from odoo import api, fields, models


class EstatePropertyTypes(models.Model):
    _name = "estate.property.type"
    _description = "Real E-state Property Type"
    _order = "sequence, name"

    name = fields.Char()
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _check_unique_property_name = models.Constraint(
        "UNIQUE(name)",
        "A property type should be unique",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
