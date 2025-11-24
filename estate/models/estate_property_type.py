from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = 'sequence, name'

    name = fields.Char('Type', required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string='Property'
    )
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_type_id', string='Offers'
    )
    offer_count = fields.Integer('Offers Count', compute='_compute_offer_count')

    _name_uniq = models.Constraint(
        'unique(name)', 'A type with the same name already exists.'
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
