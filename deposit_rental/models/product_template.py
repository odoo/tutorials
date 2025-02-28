# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    deposit_product = fields.Boolean(
        string="Deposit Product", help="Make it a deposit product."
    )
    require_deposit = fields.Boolean(
        string="Require Deposit", help="Enable if this product requires deposit.", default=False
    )
    deposit_amount = fields.Float(
        string="Amount", help="This specifies deposit for 1 unit of this product."
    )

    @api.onchange("deposit_product")
    def _onchange_deposit_product(self):
        self.require_deposit = self.deposit_product
