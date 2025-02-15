# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = 'sequence asc'
    sequence = fields.Integer(string="Sequence", default=10)

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_counts = fields.Integer(string="offer counts", compute="_compute_offer_counts")

    _sql_constraints = [
        ('check_unique_property_type', 'UNIQUE(name)',
         'Property type is already exists')
    ]

    @api.depends("offer_ids")
    def _compute_offer_counts(self):
        for record in self:
            record.offer_counts = len(record.offer_ids)
