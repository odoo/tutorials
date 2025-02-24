from odoo import fields, models, api

class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type",
        string="Properties",
    )
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    sequence = fields.Integer("Sequence")
    offer_count = fields.Integer(
            string="Offer Count",
            compute="_compute_offer_count",
            store=True
        )

    _sql_constraints = [
        ("unique_property_type", "UNIQUE(name)",
         "A property type must be unique")
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
