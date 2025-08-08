from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    require_deposit = fields.Boolean(string='Require Deposit')
    deposit_amount = fields.Float(string='Deposit Amount', help="Deposit amount for single unit.")
