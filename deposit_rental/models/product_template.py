from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    requires_deposit = fields.Boolean(string="Requires Deposit")
    deposit_amount = fields.Float()
