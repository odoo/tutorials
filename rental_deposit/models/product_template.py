from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    deposit_require = fields.Boolean(string='Require Deposit')
    deposit_amount = fields.Monetary(string='Deposit Amount')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
