# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    hello = fields.Integer()
    property_ids = fields.One2many("estate.property", "user_id", string="Real Estate Properties", domain=[('state', 'in', ('new', 'offer_received'))])
