# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = "pos.order"

    salesperson_id = fields.Many2one('hr.employee', string='Salesperson' ,help='Salesperson who created the order')
