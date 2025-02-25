# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    pos_fast_order_process = fields.Boolean(string='Fast Order Process', help="Fast Order Process when customer pay by cash")
