# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("property","salesperson_id", string="Properties linked")
    aaaa = fields.Integer()