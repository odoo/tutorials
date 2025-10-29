from odoo import models, fields
from odoo import api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence,name"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(default=10)

    # Optional: Back-reference for all properties of this type (One2many)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )

    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
        string="Offers",
    )

    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        (
            "unique_property_type_name",
            "UNIQUE(name)",
            "Property type name must be unique.",
        ),
    ]
