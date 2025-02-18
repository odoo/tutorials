from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "this is the estate property type model"
    _sql_constraints = [
        ('check_uniqueness', 'UNIQUE (name)', 'Each property type must be unique')
    ]
    _order = 'sequence'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer('Number of Offers', compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
