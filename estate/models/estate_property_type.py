# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "name asc"

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many(
        "estate.property", inverse_name="property_type_id", readonly=True
    )
    sequence = fields.Integer(string="Sequence", default=1)
    offer_ids = fields.One2many(
        "estate.property.offer", inverse_name="property_type_id"
    )
    offer_count = fields.Integer(
        string="Offer Count", default=0, compute="_compute_offer_count"
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
