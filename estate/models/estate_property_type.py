# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Type"
    _order = 'sequence, name, id'
    _sql_constraints = [
        ('uniq_name', "UNIQUE(name)", "The name must be unique."),
    ]

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence")

    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id', string="Properties")
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type_id', string="Offers")

    offer_count = fields.Integer(string="Offer Count", compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = self.env['estate.property.offer'].search_count([('property_type_id', '=', property_type.id)])
