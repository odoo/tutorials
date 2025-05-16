from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer(string="Sequence")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    offer_count = fields.Integer(compute="_compute_count_offers")

    _sql_constraints = [
        (
            "unique_property_type",
            "unique(name)",
            "A tag with same property type already exist",
        ),
    ]

    @api.depends("offer_ids")
    def _compute_count_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
