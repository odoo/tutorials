from odoo import api, fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    _order = 'sequence, name'

    name = fields.Char('Type', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer('Offer count', compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self) -> None:
        for record in self:
            record.offer_count = len(record.offer_ids)

    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name of a property type must be unique.',
    )
