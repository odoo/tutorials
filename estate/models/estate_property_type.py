from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name"

    name = fields.Char(required=True, string="Property Type")
    sequence = fields.Integer("Sequence", default=1)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The property type name must be unique")
    ]

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
