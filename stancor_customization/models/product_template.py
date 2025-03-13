# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit="product.template"

    wt_per_mt = fields.Float(string="Wt./Mtr.")
    wt_per_pc = fields.Float(string="Wt./PCs.")
