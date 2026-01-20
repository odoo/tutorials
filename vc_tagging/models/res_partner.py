# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    is_vendor = fields.Boolean(string="Is a vendor")
