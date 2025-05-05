from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )

    # Computed field to count related properties
    property_count = fields.Integer(
        string="Property Count", compute="_compute_property_count", store=True
    )

    sequence = fields.Integer(
        "Sequence", default=1, help="Order the types of properties"
    )

    offer_id = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )

    offer_count = fields.Integer(string=" Offers", compute="_compute_offer_count")

    _sql_constraints = [
        (
            "unique_property_type_name",
            "UNIQUE(name)",
            "The property Type must be unique.",
        ),
    ]

    @api.depends("property_ids")
    def _compute_property_count(self):
        for rec in self:
            rec.property_count = len(rec.property_ids)

    @api.depends("offer_id")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_id)
