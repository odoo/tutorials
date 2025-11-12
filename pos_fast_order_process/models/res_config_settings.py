# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_fast_order_process = fields.Boolean(related='pos_config_id.pos_fast_order_process', readonly=False)
