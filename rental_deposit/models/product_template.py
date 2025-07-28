from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    require_deposit = fields.Boolean(string="Require Deposit", default=False)
    deposit_amount = fields.Float(string="Amount")
