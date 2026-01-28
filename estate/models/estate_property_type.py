from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type Information'
    _order = 'sequence, name asc'

    name = fields.Char(string='Property Type', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer(string='Sequence', default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")

    offer_count = fields.Integer(compute='_compute_offer_count', string='Offer Count')

    _check_type_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The property type name must be unique.'
    )

    @api.depends('property_ids.offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
