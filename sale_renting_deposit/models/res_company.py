# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    deposit_product = fields.Many2one(comodel_name='product.product', string="Deposit Product")
