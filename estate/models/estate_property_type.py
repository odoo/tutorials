from odoo import models, fields, api


class EstatePropertyType(models.Model):

    _name = 'estate.property.type'
    _description = 'Estate Property Types'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer()
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string='\n', compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'This property type already exists.'),
    ]
