from odoo import fields, models, api


class EstateType(models.Model):
    _name = "estate.property.type"
    _description = "property type"
    _order = "sequence"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', inverse_name='property_type_id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages.")
    offer_ids = fields.One2many("estate.property.offer", inverse_name='property_type_id')
    offer_count = fields.Integer(compute="_compute_count_offer")

    @api.depends("offer_ids")
    def _compute_count_offer(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
