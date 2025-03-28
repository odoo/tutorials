from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'
    _order = 'sequence, name'
    _sql_constraints = [(
        'type_name_unique', 'UNIQUE(name)',
        'Type name should be unique.'
    )]

    name = fields.Char('Name', required=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string ='Offers')
    offer_count = fields.Integer('Offer count', compute='_compute_offer_count')
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence', default=1)

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
