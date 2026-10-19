from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    sequence = fields.Integer()
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer(compute="_compute_offer_count")

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The name of the property type must be unique",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
