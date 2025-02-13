from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'
    _order = 'name'

    name = fields.Char(string='Title', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offer')
    offer_count = fields.Integer(compute='_compute_offer_count', string='Offer count')

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'Property type must be unique.')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
