from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_deposit = fields.Boolean(string='Require Deposit')
    deposit_amount = fields.Float(string='Amount')
