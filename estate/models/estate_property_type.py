from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "description"
    _order = "sequence, name"

    name = fields.Char("Type", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order types.")

    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_distinct_offers')

    @api.depends("offer_ids")
    def _compute_distinct_offers(self):
        self.offer_count = len(self.offer_ids)
