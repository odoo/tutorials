from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    required_deposit = fields.Boolean(default=False)
    amount_deposit = fields.Float(string="Deposit Amount")
