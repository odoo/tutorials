# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(required=True, copy=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types.")
    
    property_count = fields.Integer(string="Properties Count", compute='_compute_property_count')

    _sql_constraints = [
       ('unique_property_type_name', 'UNIQUE(name)', 'The property type name must be unique!')
    ]

    @api.depends('property_ids')
    def _compute_property_count(self):
        for ptype in self:
            ptype.property_count = len(ptype.property_ids)
    
    def action_view_properties(self):
        self.ensure_one()
        return {
            'name': f"Properties for Type: {self.name}",
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property',
            'view_mode': 'list,form',
            'domain': [('property_type_id', '=', self.id)],
            'context': {'default_property_type_id': self.id}
        }
