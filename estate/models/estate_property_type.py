from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Defines the type of Real Estate Property'
    _order = 'name'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate_property', 'property_type_id', string='Properties')
    sequence = fields.Integer(
        default=1,
        help='used to order the type based on the number of time it is used'
    )
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offers_count')

    _check_unique_name = models.Constraint(
        'unique(name)',
        'A tag with the same name already exists.'
    )

    @api.depends('offer_ids')
    def _compute_offers_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
