# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)',
         'The property type name must be unique.'),
    ]

    name = fields.Char(string='Property Type', required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', readonly=True)
    sequence = fields.Integer(string='Sequence', default=1,
                              help='Used to order stages. Lower is better.')
    offer_ids = fields.One2many(
        string='Offers',
        comodel_name='estate.property.offer',
        inverse_name='property_type_id'
    )
    offer_count = fields.Integer(
        string='Offer Count', compute='_compute_offers', store=True)

    @api.depends('offer_ids')
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_open_offers(self):
        return {
            'name': 'Offers',
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.offer',
            'view_mode': 'list,form',
            'domain': [('property_type_id', '=', self.id)],
            'context': {'default_property_type_id': self.id},
        }
