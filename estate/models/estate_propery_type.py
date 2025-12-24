from odoo import models, fields, api


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Defines the property type: house, apartment, penthouse, castle, etc.'
    _order = 'sequence, name'

    name = fields.Char('Name', required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string='Properties')

    offer_ids = fields.One2many(
        'estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(
        string="Offer Count", compute='_compute_offer_count')

    sequence = fields.Integer('Sequence', default=1,
                              help='Used to order property type')

    _sql_constraints = [('unique_name',
                        'unique(name)', 'Name must be unique')]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids) if hasattr(
                record, 'offer_ids') else 0
