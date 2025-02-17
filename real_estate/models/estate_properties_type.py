# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstatePropertiesType(models.Model):
    _name = 'estate.properties.type'
    _description = 'Estate Properties Type'
    _order = 'name'
    _sql_constraints = [
        ('name', 'UNIQUE(name)',
         'Property Type should be unique')
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.properties', 'property_type_id', string='Properties')
    sequence = fields.Integer()
    offer_ids = fields.One2many(
        'estate.properties.offer', 'property_type_id', string='Offer')
    offer_count = fields.Integer(compute='_compute_offer_count', store=True)

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def redirect_offer_form(self):
        return {
            'name': 'Offer',
            'type': 'ir.actions.act_window',
            'res_model': 'estate.properties.offer',
            'views': [[False, 'list'], [False, 'form']],
            'target': 'current',
            'domain': [['property_type_id', '=', self.id]],
            'context': [['default_property_type_id', '=', self.id]],
        }
