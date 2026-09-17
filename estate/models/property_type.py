from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property types"
    _order = "sequence, name"

    sequence = fields.Integer(string="Sequence", default=1)
    name = fields.Char(required=True, string="Name")
    property_ids = fields.One2many("estate.property", inverse_name="property_type_id")
    offer_ids = fields.One2many(
        "estate.property.offer",
        inverse_name="property_type_id",
    )
    offer_count = fields.Integer(compute="_compute_offer_counts")

    @api.depends("offer_ids")
    def _compute_offer_counts(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
