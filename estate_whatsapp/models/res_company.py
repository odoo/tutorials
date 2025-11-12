# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    wa_sale_template_id = fields.Many2one('whatsapp.template', string='WhatsApp Template', domain=[
        ('model', '=', 'estate.properties'), ('status', '=', 'approved')])
