from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Adds different property types"
    _sql_constraints = [
        (
            "property_type_unique",
            "UNIQUE (name)",
            "Property Type already exists.",
        ),
    ]
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer(
        compute="_compute_offer_count", string="Number of Offers"
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
