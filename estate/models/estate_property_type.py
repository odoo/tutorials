# -*- coding: utf-8 -*-
from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate_property_type'
    _description = 'Real Estate Property Type'
    _order = 'name'

    name = fields.Char(required=True)
    offer_ids = fields.One2many(
        'estate_property_offer',
        'property_type_id',
        string='Offers'
    )
    offer_count = fields.Integer(
        compute='_compute_offer_count',
        store=True
    )
    sequence = fields.Integer(default=1)

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    def action_open_offers(self):
        return {
            'name': 'Offers',
            'type': 'ir.actions.act_window',
            'res_model': 'estate_property_offer',
            'view_mode': 'tree,form',
            'domain': [('property_type_id', '=', self.id)],
            'context': {
                'default_property_type_id': self.id
            }
        }

    _sql_constraints = [(
        'check_unique_name',
        'UNIQUE(name)',
        'this name already exists!')
    ]

    property_ids = fields.One2many(
        'estate_property',
        'property_type_id',
        string='Properties'
    )
