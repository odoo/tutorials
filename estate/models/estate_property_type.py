from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'A type of property'
    _order = 'sequence asc'

    name = fields.Char(string='Title', required=True)
    _unique_name = models.Constraint('UNIQUE(name)', 'The name must be unique.')
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string='Properties'
    )
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
