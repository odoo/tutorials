# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class InheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        comodel_name="estate.property", inverse_name="property_seller_id", domain=[("state", "in", ["new", "offer received"])])
