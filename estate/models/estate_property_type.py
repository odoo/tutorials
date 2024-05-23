from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1, help="Used to order property types")

    property_ids = fields.One2many("estate.property", inverse_name="property_type_id")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_type_id")

    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids) or 0
