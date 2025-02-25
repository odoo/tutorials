# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    company_id = fields.Many2one(
        'res.company',
        string="company",
        ondelete='cascade')
    wa_sale_template_id = fields.Many2one(
        related='company_id.wa_sale_template_id', readonly=False, store=True)
