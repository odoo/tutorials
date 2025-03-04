# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_deposit_required = fields.Boolean(string="Require Deposit")
    deposit_amount = fields.Float(string="Deposit Amount")
