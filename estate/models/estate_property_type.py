from odoo import api, fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence')
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offers_count')

    _sql_constraints = [
        ('type_unique_name', 'unique(name)', 'The type name must be unique')
    ]

    @api.depends('offer_ids')
    def _compute_offers_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
