# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"
    _order = 'sequence, name'
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', "Property type name must be unique!")
    ]

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id', string="Properties")
    sequence = fields.Integer(string="Sequence")
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type_id', string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
