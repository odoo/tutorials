# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Type"
    _explanation = "Defines a real estate property type"
    _order = "sequence"

    name = fields.Char('Property Type', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Type Properties')
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Type Offers')
    offer_count = fields.Integer(compute='_compute_offer_count', store=True)

    _check_unique = models.Constraint(
        'UNIQUE(name)',
        'A property type with that name already exists.',
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        self.ensure_one()
        self.offer_count = len(self.offer_ids)
