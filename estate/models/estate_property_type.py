from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'name'

    name = fields.Char(string='Property Type', required=True)
    sequence = fields.Integer('Sequence', default=1, help='Used to order offer types. Lower is better.')
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Properties offers')
    offer_count = fields.Integer(compute='_compute_offer_count', string='Offers Count')

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
