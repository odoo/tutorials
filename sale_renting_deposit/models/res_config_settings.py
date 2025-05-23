# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_product = fields.Many2one(
        string="Deposit Product",
        help="This product will be used in rental order for deposit amount.",
        comodel_name='product.product',
        related='company_id.deposit_product',
        readonly=False,
        domain=[('type', '=', 'service')],
    )
