# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    add_to_report = fields.Boolean(string="Print in Report?")
