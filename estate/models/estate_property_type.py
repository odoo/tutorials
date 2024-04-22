from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate property type"
    _order = "name"
    _sql_constraints = [
        (
            "unique_property_type",
            "UNIQUE(name)",
            "The property type must be unique",
        )
    ]

    name = fields.Char("Title", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer()
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_total_offers")

    @api.depends("offer_ids")
    def _compute_total_offers(self):
        for record in self:
            # print("#####")
            # print(record.offer_ids)
            record.offer_count = len(record.offer_ids)
