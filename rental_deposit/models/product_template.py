from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    require_deposit = fields.Boolean(string="Require Deposit")
    deposit_amount = fields.Float(string="Deposit Amount")

    @api.onchange('require_deposit')
    def _onchange_require_deposit(self):
        self.write({
            'deposit_amount': 0 if self.require_deposit else 0
        })
