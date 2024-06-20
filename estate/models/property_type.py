# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api

class PropertyType(models.Model):
    _name = "property.type"
    _description = "Property types of a Real Estate"
    _order = "sequence"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many("property.offer", "property_type_id", "Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints  = [
        ('check_unique_type', 'unique (name)', 'Odoopsie! This name is already chosen' )
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self) :
        for property_type in self :
            property_type.offer_count = len(property_type.offer_ids)