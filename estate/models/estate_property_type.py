from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property types"
    _order = "sequence"

    name = fields.Char("Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer("Count", compute="_compute_offer_count")

    _uniq_name = models.Constraint(
        "UNIQUE(name)",
        "This name is already taken",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
