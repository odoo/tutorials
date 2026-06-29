from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property"
    _order = "sequence, name"

    name = fields.Char(required=True)
    line_ids = fields.One2many(
        "estate.property",
        "property_type_id"
    )
    sequence = fields.Integer(default=1)
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers"
    )
    offer_count = fields.Integer(compute="_compute_offer_count")

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
