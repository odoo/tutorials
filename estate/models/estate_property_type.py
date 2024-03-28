from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"
    _sql_constraints = [
        ("check_unique_name", "UNIQUE(name)",
        "A property tag name must be unique")
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "type_id")
    sequence = fields.Integer("Sequence")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offers_count")

    @api.depends("offer_ids")
    def _compute_offers_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
