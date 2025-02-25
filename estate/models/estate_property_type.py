# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Type"
    _order = 'sequence'
    _sql_constraints = [
        ('check_unique_property_type', 'UNIQUE(name)',
         'Property type is already exists')
    ]

    name = fields.Char(string="Property Type", required=True)
    offer_counts = fields.Integer(string="offer counts", compute='_compute_offer_counts')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer(string="Sequence", default=10)

    @api.depends('offer_ids')
    def _compute_offer_counts(self):
        for property_type in self:
            property_type.offer_counts = len(property_type.offer_ids)
