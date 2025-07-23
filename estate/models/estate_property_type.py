from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"

    _sql_constraints = [
        (
            "check_unique",
            "UNIQUE(name)",
            "There is already a property type with this name.",
        )
    ]

    _order = "name"

    name = fields.Char("Type", required=True)

    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    sequence = fields.Integer("Sequence", default=1)

    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")

    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for prop_type in self:
            prop_type.offer_count = len(prop_type.offer_ids)
