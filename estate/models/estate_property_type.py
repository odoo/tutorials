from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _sql_constraints = [
        (
            "unique_property_type_name",
            "UNIQUE(name)",
            "The name of tag must be unique.",
        ),
    ]
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many(related="property_ids.offer_ids")
    offer_count = fields.Integer(compute="_compute_offer_count")
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order types. Lower is better."
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for prp in self:
            pricelist = prp.mapped("offer_ids")
            prp.offer_count = len(pricelist)
