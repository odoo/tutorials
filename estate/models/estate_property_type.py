from datetime import timedelta
from odoo import api, exceptions, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of Properties are stored"
    _order = "sequence, name"

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
    sequence = fields.Integer(default=1)
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.today() + timedelta(days=90)
    )
    selling_price = fields.Integer(
        "Selling Price", readonly=True, copy=False, default=1000000
    )
    property_ids = fields.One2many(
        "estate.property", "property_type_id"
    )  # """string="Properties)
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer(
        string="Offer Count", compute="_compute_offer_count", store=True
    )

    _sql_constraints = [
        (
            "unique_property_type_name",
            "UNIQUE(name)",
            "The property type name must be unique.",
        )
    ]
