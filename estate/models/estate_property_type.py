# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Used to describe the type of the property i.e House, Apartment, etc."
    _order = "name"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer('Sequence', default=1)
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Type with this name already exists, try another name.')
    ]

    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='property_type_id'
        )

    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_type_id'
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
