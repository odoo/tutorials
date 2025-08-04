# imports of odoo
from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property types for available in the business.'
    _order = 'sequence, name'

    # SQL Constraints
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Type name must be unique.')
    ]

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=10)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string='Number of Offers', compute='_compute_offer_count')

    # === Compute methods ===
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        '''Compute the number of offers linked to each property type.

        This method calculates the total number of related offers (`offer_ids`)
        for each type in the `estate.property.type` model and stores the count
        in the `offer_count` field.
        '''
        for record in self:
            record.offer_count = len(record.offer_ids) if hasattr(
                record, 'offer_ids') else 0
