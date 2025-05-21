from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _sql_constraints = [
        (
            "estate_property_type_name_unique",
            "UNIQUE(name)",
            "The type names must be unique.",
        )
    ]

    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence")
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(
        compute="_compute_offer_count", string="Offer Count", readonly=True, copy=False
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
