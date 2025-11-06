from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'type_id')
    sequence = fields.Integer(string="Sequence", default=1)
    offer_count = fields.Integer(compute="_compute_total_offers")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")

    @api.depends("offer_ids")
    def _compute_total_offers(self):
        for record in self:
            record.offer_count = len(record.property_ids.mapped("offer_ids"))
