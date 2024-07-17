from odoo import models, fields, api


class EstateTypeModel(models.Model):
    _name = 'estate.type'
    _description = "Real estate types model"
    _order = 'type, sequence'

    type = fields.Char()
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offers_count = fields.Integer(compute='_computed_offers_count')

    @api.depends('offer_ids')
    def _computed_offers_count(self):
        for rec in self:
            rec.offers_count = len(rec.offer_ids)

    _sql_constraints = [
        ('unique_type', 'UNIQUE(type)',
         'Expected type to be unique'),
    ]
